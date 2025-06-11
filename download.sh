#!/bin/bash

mkdir -p models

# Download all models from Google Drive using wget
wget "https://drive.google.com/uc?export=download&id=1dvKoq8wMc_xqXtDHQX7rnc0n4PTsQOa0" -O models/yolo11x.pt
wget "https://drive.google.com/uc?export=download&id=1XCN68J8d2C_DbB2F8ak6AOOF7wyfaufO" -O models/yolov10l.pt
wget "https://drive.google.com/uc?export=download&id=1Hz8IVZ8YR47Ly0smoOHkmvnf6g1bB4ee" -O models/yolov8x-oiv7.pt
wget "https://drive.google.com/uc?export=download&id=156UHX51YScgFby-m5r1yWH6TqRf-AH6B" -O models/yolov9e.pt
wget "https://drive.google.com/uc?export=download&id=1_8k9WBojdexUUA6l69YYrOZCGG8TBSks" -O models/backup.pt
