# SerenEnhance

This is our implementation for the SIGIR 2023 paper: 

**Fu, Z., Niu, X. and Yu, L., 2023, July. Wisdom of Crowds and Fine-Grained Learning for Serendipity Recommendations. In _Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval_ (pp. 739-748).** [[Paper]](https://dl.acm.org/doi/10.1145/3539618.3591787)

**Dataset:**  
1. _SerenLens_ [[link]](https://github.com/zhefu2/SerenLens), a large ground truth dataset on serendipity-oriented recommendation.
2. Amazon Review Data (Books). [[link]](https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/)

 ## Files

- Unexpectedness_generation.py: Calculating unexpectedness score for each user-item pair.
- SerenEnhance.py: Our proposed model.

## Environment Settings
 We use Tensorflow as the backend.
 * Tensorflow version: '2.8.0'
 
## Quick Start

1. Pre-calculate the items' unexpectedness scores for each user and generate the unexpectedness training set
    ```
    python Unexpectedness_generation.py
    ```
    
2. Train the SerernEnhance model (The training data can be found [here](https://drive.google.com/drive/folders/10zNYgfyoe5NVJM3uPUZTTuOEDzG7sHuu?usp=sharing))
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
