1. <b> Архитектура: </b>

  SkipGram with Hierarchical Softmax
  
2. <b> Функции: </b>

  ●	fit(documents: List(List(String))) -> None
  
  ●	get_words() -> List(String) - словарь
  
  ●	get_emb(word: String) -> np.ndarray - получение эмбеддинга
  
  ●	get_similar(word: String,  k:Int) -> List(String) - список ближайших слов (синонимы)
  
  ●	save_state(path: String)
  
  ●	load_state(path: String)
  
3. <b> Обучение: </b>

  Обучено на коротеньком "Франкенштейне" (всего 2860 слов) - время обучения 35-40 секунд
  
4. <b> Тестирование: </b>

  ●	Similarity: на основе https://github.com/EloiZ/embedding_evaluation/tree/master/data
  
   Используются датасеты: MEN, WordSim-353, Verb-143. Нормальная корреляция только с ws353.
    
  ●	Pos Tagging: логрег на данных conll2000  
  
   Accuracy: 0.71 - если предсказывать трейн и тест как есть (есть повторения слов и внутри и между датасетами).
   
   <b> 0.23 </b> - если взять все уникальные слова и поделить 60:30 (>20 частей речи, 9 популярных, т.е. лучше рандома).
    
5. <b> Красивые картинки: </b>
![image](https://user-images.githubusercontent.com/20374616/58386813-fda6ad80-800d-11e9-8eff-cd8d8d14aca8.png)
![image](https://user-images.githubusercontent.com/20374616/58388149-7f550600-8023-11e9-92ba-3bf444080526.png)
