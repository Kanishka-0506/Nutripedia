#!/bin/bash

mkdir -p uploads

echo "Downloading models..."

wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1dvKoq8wMc_xqXtDHQX7rnc0n4PTsQOa0' -O uploads/yolo11x.pt
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1XCN68J8d2C_DbB2F8ak6AOOF7wyfaufO' -O uploads/yolov10l.pt
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1Hz8IVZ8YR47Ly0smoOHkmvnf6g1bB4ee' -O uploads/yolov8x-oiv7.pt
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=156UHX51YScgFby-m5r1yWH6TqRf-AH6B' -O uploads/yolov9e.pt

echo "All downloads finished."
