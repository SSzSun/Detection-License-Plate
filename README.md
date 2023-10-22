# Detection-License-Plate
### โปรแกรมนี้เป็นส่วนนึงของวิชา Image
------
```bash
git clone https://github.com/SSzSun/Detection-License-Plate.git
```
------
รายละเอียดไฟล์
* Folder Model เก็บรายละเอียด Model ป้ายทะเบียน 
  * eng_epr3   : epochs=3
  * eng_epr20  : epochs=20
* Folder dataset_lic ะเก็บไฟล์นามสกุล yaml เอาไว้สำหรับใช้กับโมเดล YOLOv8 ในตัวโปรแกรมของเรา
* Folder vedio ใช้เก็บวิดิโอที่จะทดสอบ
* File main.py เป็นโปรแกรมหลักในการใช้รันโปรแกรม
* File util.py ใช้สำหรับอ่านตัวอักษรบนป้ายทะเบียน โดยใช้ easyocr ในการเช็ค
* File visualize.py เป็นไฟล์ไว้ทำ VideoWriter เพื่อเขียนสิ้งที่ตรวจเจอให้เห็น โดยใช้ข้อมูลจาก test_interpolated.csv ในการทำงาน
* File train.py เอาไว้ Train Dataset
* File add_missing_data.py เป็นเพื่อเพิ่มข้อมูลที่สูญหาย และ output ออกมาเป็น test_interpolated.csv
* File test.csv เป็นข้อมูลสถิติที่ตรวจพบ
* File test_interpolated.csv เป็นไฟล์ที่ผ่านการแก้ไขหรือหลังจากทำข้อมูลใหม่
----
