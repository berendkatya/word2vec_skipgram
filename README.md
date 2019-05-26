1. <b> Архитектура: </b>
  SkipGram Hierarchical Softmax
2. <b> Функции: </b>
  ●	fit(documents: List(List(String))) -> None
  ●	get_words() -> List(String) - словарь
  ●	get_emb(word: String) -> np.ndarray - получение эмбеддинга
  ●	get_similar(word: String,  k:Int) -> List(String) - список ближайших слов (синонимы)
  ●	save_state(path: String)
  ●	load_state(path: String)
3. <b> Обучение: </b>
  Обучено на коротеньком "Франкенштейне" (всего 2860 слов)
4. <b> Тестирование: </b>
  ●	Similarity: на основе https://github.com/EloiZ/embedding_evaluation/tree/master/data
    Используются датасеты: MEN, WordSim-353, Verb-143.
    Нормальная корреляция только с ws353.
  ●	Pos Tagging: логрег на данных conll2000
    
5. <b> Красивая картинка: </b>
![image](https://user-images.githubusercontent.com/20374616/58386813-fda6ad80-800d-11e9-8eff-cd8d8d14aca8.png)
