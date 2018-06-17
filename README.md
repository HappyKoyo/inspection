# Robot Inspection 2018 in Canada
## Overview
RoboCup2018 Canada Montreal@home  
Robot Inspection用のスクリプト.  

## Writter
1. Enomoto

--------------------------------------
# 大会チェックリスト:triangular_flag_on_post:
## ハードウェア
- [ ] USB+イヤホンジャックが刺さっているかを確認
- [ ] 緊急停止スイッチOFF
- [ ] PC起動後にスピーカーの電源ON、スピーカーのLEDが**青く光っているか**を確認
- [ ] adjust speacker boryu-mu
- [ ] スピーカーの電源が、繋がっている.
- [ ] 設定->サウンド->入力装置->内部オーディオを消音にし、MobilePreをONにする
- [ ] MobilePreマイクに触れて、動作していることを確認する
- [ ] 音声の出力をunavailableにする
- [ ] `sh mic_check.sh`(一度エラーが起こる)
- [ ] 機体のスイッチをONにする
- [ ] 充電器を抜く
## ソフトウェア  
```
    ~/catkin_ws/src/inspection/scripts/sh start_inspection.sh
    rosrun inspection EInspection
```

--------------------------------
