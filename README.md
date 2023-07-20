# SerenEnhance

This is our implementation for the SIGIR 2023 paper: 

**Fu, Z., Niu, X. and Yu, L., 2023, July. Wisdom of Crowds and Fine-Grained Learning for Serendipity Recommendations. In _Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval_ (pp. 739-748).** [[Paper]](https://dl.acm.org/doi/10.1145/3539618.3591787)

**Dataset:**  _SerenLens_ [[link]](https://github.com/zhefu2/SerenLens), a large ground truth dataset on serendipity-oriented recommendation.

 ## Files

- Data. Training and testing data.
- Unexpectedness generation.py. Calculating unexpectedness score for each user-item pair.
- SerenEnhance.py: Our proposed model.

## Environment Settings
 We use Tensorflow as the backend.
 * Tensorflow version: '2.8.0'
 
## Quick Start

1. Pre-calculate the items' unexpectedness scores for each user
    ```
    cd Data
    gunzip *
    ```
2. Prepare the relevance training set and unexpectedness training set
    ```
    python training_data.py
    ```
    
3. Train the SerernEnhance model
    ```
    python SerenEnhance.py
    ```
 

## Reference
Fu, Z., Niu, X. and Yu, L., 2023, July. Wisdom of Crowds and Fine-Grained Learning for Serendipity Recommendations. In _Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval_ (pp. 739-748).


```  
@inproceedings{fu2023wisdom,
  author    = {Fu, Zhe and Niu, Xi(Sunshine) and Yu, Li},
  title     = {Wisdom of Crowds and Fine-Grained Learning for Serendipity Recommendations},
  booktitle = {Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval},
  pages     = {739--748},
  publisher = {{ACM}},
  year      = {2023}
}
```
