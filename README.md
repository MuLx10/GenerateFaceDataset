# GenerateFaceDataset

## Scrape Data
```
 $ python googleScrape.py --keywords "Sloth Bear, baloons, Beaches" --limit 20
 $ python googleScrape.py -k "Mr Bean, baloons, Beaches" -l 20 --type animated
 $ python googleScrape.py --keywords "Sara Santini" --limit 100

```

## Face Recognition

```
$ python face_detection.py --input downloads/MrBean/ --output data/MrBean/
$ python face_detection.py -i downloads/SaraSantini/ -o data/SaraSantini/

```