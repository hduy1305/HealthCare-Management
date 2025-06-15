
# HealthCare Management System 🏥

Một hệ thống quản lý y tế hiện đại được phát triển theo kiến trúc **microservices**, hỗ trợ quy trình khám chữa bệnh, đặt lịch, lưu trữ hồ sơ bệnh án và thanh toán một cách hiệu quả.

## 🔧 Kiến trúc tổng quan

Dự án được thiết kế gồm nhiều service độc lập giao tiếp với nhau và **RESTful APIs**. Mỗi service đảm nhận một chức năng riêng biệt và sử dụng cơ sở dữ liệu phù hợp với nghiệp vụ.

![Component Diagram](assets/Component%20Diagram1.jpg)


---

## 🧩 Các Microservices

### 1. `user_service`
- **Chức năng**:
  - Đăng ký / Đăng nhập người dùng
  - Xác thực và phân quyền (bệnh nhân, bác sĩ, quản trị viên)
- **Cơ sở dữ liệu**: MySQL
- **Trạng thái**: ✅ Hoàn thành

---

### 2. `patient_service`
- **Chức năng**:
  - Quản lý thông tin cá nhân bệnh nhân
  - Quản lý lịch sử khám chữa bệnh
- **Cơ sở dữ liệu**: MySQL
- **Trạng thái**: ✅ Hoàn thành

---

### 3. `doctor_service`
- **Chức năng**:
  - Quản lý hồ sơ bác sĩ
  - Lịch làm việc, chuyên khoa
  - Kê đơn thuốc, chẩn đoán
- **Cơ sở dữ liệu**: MySQL
- **Trạng thái**: ✅ Hoàn thành

---

### 4. `appointment_service`
- **Chức năng**:
  - Đặt lịch khám giữa bệnh nhân và bác sĩ
  - Quản lý, cập nhật lịch hẹn
- **Cơ sở dữ liệu**: MySQL
- **Trạng thái**: ✅ Hoàn thành

---

### 5. `medical-record_service` *(Đang phát triển)*
- **Chức năng**:
  - Lưu trữ hồ sơ bệnh án điện tử (EHR)
  - Kết quả xét nghiệm, chẩn đoán hình ảnh
- **Cơ sở dữ liệu**: MongoDB
- **Trạng thái**: 🚧 Đang phát triển

---

### 6. `payment_service` *(Đang phát triển)*
- **Chức năng**:
  - Xử lý thanh toán viện phí
  - Hóa đơn, bảo hiểm y tế
- **Cơ sở dữ liệu**: MySQL
- **Trạng thái**: 🚧 Đang phát triển

---

### 7. `notification_service` *(Đang phát triển)*
- **Chức năng**:
  - Gửi email, SMS nhắc lịch hẹn, thông báo kết quả
- **Công nghệ**: Firebase / Redis
- **Trạng thái**: 🚧 Đang phát triển

---

## 🛠️ Công nghệ sử dụng

- **Ngôn ngữ**: Python 3.x  
- **Framework**: Django, Django REST Framework  
- **Cơ sở dữ liệu**:
  - MySQL: cho các service dạng quan hệ (user, patient, doctor, appointment, payment)
  - MongoDB: cho `medical-record-service` (phi quan hệ, lưu trữ EHR)
  - Redis / Firebase: cho `notification-service`
- **API Gateway**: Django (hiện tại chưa sử dụng, phục vụ cho mục đích phát triển sau này)
- **Authentication**: JWT (JSON Web Tokens)
- **Triển khai**:
  - Docker, Docker Compose: quản lý container và orchestrate multi-service
  - `.env` cho biến môi trường từng service

## Khởi chạy dự án

- docker-compose up --build

<<<<<<< HEAD
---
## Bản quyền
- Ngô Hoàng Duy
=======
## Bản quyền
>>>>>>> 229c7d5 (update records service)

- Ngô Hoàng Duy