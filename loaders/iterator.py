import json
import os
from typing import Iterable, Callable
from tqdm import tqdm


class ResumableIterator:
    def __init__(self, iterable: Iterable, checkpoint: str = "progress.json", batch_size: int = 10):
        self.items = list(iterable)
        self.checkpoint = checkpoint
        self.batch_size = batch_size
        self.done = set()
        self._load_progress()

    def _load_progress(self):
        if os.path.exists(self.checkpoint):
            try:
                with open(self.checkpoint, "r") as f:
                    self.done = set(json.load(f))
            except Exception:
                self.done = set()

    def _save_progress(self):
        with open(self.checkpoint, "w") as f:
            json.dump(list(self.done), f)

    def run(self, func: Callable):
        """
        Iterate over items and apply func(item).
        Saves progress every `batch_size` successes.
        """
        batch_count = 0

        with tqdm(total=len(self.items),
                  desc="Processing",
                  initial=len(self.done)
            ) as pbar:

            for item in self.items:
                if item in self.done:
                    continue  # skip already processed

                try:
                    func(item)
                    self.done.add(item)
                    batch_count += 1
                    pbar.update(1)

                    # save after batch
                    if batch_count >= self.batch_size:
                        self._save_progress()
                        batch_count = 0

                except Exception as e:
                    print(f"❌ Error with {item}: {e}")
                    print("Progress saved. Resume later with same checkpoint.")
                    self._save_progress()
                    break

            # final save if needed
            if batch_count > 0:
                self._save_progress()