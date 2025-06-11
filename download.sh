#!/bin/bash

mkdir -p uploads

wget "https://drive.google.com/uc?export=download&id=1dvKoq8wMc_xqXtDHQX7rnc0n4PTsQOa0" -O uploads/yolo11x.pt
wget "https://drive.google.com/uc?export=download&id=1XCN68J8d2C_DbB2F8ak6AOOF7wyfaufO" -O uploads/yolov10l.pt
wget "https://drive.google.com/uc?export=download&id=1Hz8IVZ8YR47Ly0smoOHkmvnf6g1bB4ee" -O uploads/yolov8x-oiv7.pt
wget "https://drive.google.com/uc?export=download&id=156UHX51YScgFby-m5r1yWH6TqRf-AH6B" -O uploads/yolov9e.pt
wget "https://drive.google.com/uc?export=download&id=1_8k9WBojdexUUA6l69YYrOZCGG8TBSks" -O uploads/backup.pt
