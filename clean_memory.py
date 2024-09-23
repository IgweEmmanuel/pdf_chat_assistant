import gc
import torch
import load_transformers
del load_transformers.model
del load_transformers.tokenizer


torch.cuda.empty_cache()
gc.collect()
torch.cuda.reset_peak_memory_stats()
torch.cuda.empty_cache()
