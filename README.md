# SerenEnhance

This is our implementation for the SIGIR 2023 paper: 

**Fu, Z., Niu, X. and Yu, L., 2023, July. Wisdom of Crowds and Fine-Grained Learning for Serendipity Recommendations. In _Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval_ (pp. -).** [[Paper]]()

**Dataset:**  _SerenLens_ [[link]](https://github.com/zhefu2/SerenLens), a large ground truth dataset on serendipity-oriented recommendation.

 ## Files

- Data. Training and testing data.
    - yelp.train.rating. Rating of training data.
    - yelp.test.rating. Rating of testing data.
    - yelp.test.negative. 1000 testing samples for each user. (0,32) means this row is for user 0 and the positive test item is 32.
- Dataset.py. Module preprocessing data.
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
Fu, Z., Niu, X. and Yu, L., 2023, July. Wisdom of Crowds and Fine-Grained Learning for Serendipity Recommendations. In _Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval_ (pp. *-*).


```  
@inproceedings{fu2023wisdom,
  author    = {Fu, Zhe and Niu, Xi(Sunshine) and Yu, Li},
  title     = {Wisdom of Crowds and Fine-Grained Learning for Serendipity Recommendations},
  booktitle = {Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval},
  pages     = {*--*},
  publisher = {{ACM}},
  year      = {2023}
}
```
