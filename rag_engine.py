"""
RAG Engine для обработки PDF документов и поиска ответов
"""
import pdfplumber
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from pathlib import Path
from typing import List, Tuple


class RAGEngine:
    def __init__(self, documents_dir: str = "documents"):
        self.documents_dir = documents_dir
        self.chunks: List[str] = []
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.chunk_vectors = None
        self.is_initialized = False
        
    def load_documents(self) -> List[str]:
        """Загружает все PDF документы из директории"""
        all_text = []
        pdf_files = list(Path(self.documents_dir).glob("*.pdf"))
        
        if not pdf_files:
            print(f"️ PDF файлы не найдены в {self.documents_dir}")
            return []
        
        print(f"📚 Найдено {len(pdf_files)} PDF файлов")
        
        for pdf_file in pdf_files:
            print(f"  📄 Обрабатываю: {pdf_file.name}")
            try:
                with pdfplumber.open(pdf_file) as pdf:
                    for page_num, page in enumerate(pdf.pages, 1):
                        text = page.extract_text()
                        if text:
                            # Разбиваем текст на чанки по абзацам
                            paragraphs = text.split('\n\n')
                            for paragraph in paragraphs:
                                if len(paragraph.strip()) > 50:  # Пропускаем короткие фрагменты
                                    all_text.append(paragraph.strip())
            except Exception as e:
                print(f"  ❌ Ошибка обработки {pdf_file.name}: {e}")
        
        print(f"✅ Загружено {len(all_text)} текстовых блоков")
        return all_text
    
    def initialize(self):
        """Инициализирует векторное хранилище"""
        print("🔄 Инициализация RAG движка...")
        self.chunks = self.load_documents()
        
        if not self.chunks:
            print("⚠️ Нет данных для инициализации")
            return
        
        # Создаем векторное представление
        self.chunk_vectors = self.vectorizer.fit_transform(self.chunks)
        self.is_initialized = True
        print(f"✅ RAG движок готов! Обработано {len(self.chunks)} блоков")
    
    def search_relevant_chunks(self, query: str, top_k: int = 3) -> List[str]:
        """Ищет наиболее релевантные фрагменты для запроса"""
        if not self.is_initialized:
            return ["База знаний не загружена. Пожалуйста, загрузите PDF документы."]
        
        # Векторизуем запрос
        query_vector = self.vectorizer.transform([query])
        
        # Вычисляем сходство
        similarities = cosine_similarity(query_vector, self.chunk_vectors)[0]
        
        # Получаем топ-K наиболее похожих чанков
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        relevant_chunks = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Минимальный порог сходства
                relevant_chunks.append(self.chunks[idx])
        
        return relevant_chunks
    
    def get_context(self, query: str) -> str:
        """Получает контекст для запроса"""
        chunks = self.search_relevant_chunks(query)
        if not chunks:
            return "Информация не найдена в базе знаний."
        
        # Объединяем чанки в контекст
        context = "\n\n".join(chunks)
        return context


# Глобальный экземпляр движка
rag_engine = RAGEngine()
