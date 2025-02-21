# Encryptor
# **File Encryption & Decryption Software**

## **Giới thiệu**

Phần mềm này giúp người dùng **mã hóa** và **giải mã** các file với **mật khẩu bảo mật**, nhằm bảo vệ dữ liệu cá nhân và tài liệu quan trọng khỏi sự truy cập trái phép. Phần mềm tích hợp trực tiếp vào **Windows File Explorer**, cho phép người dùng thực hiện thao tác mã hóa và giải mã **bằng chuột phải** vào file mong muốn mã hóa hoặc giải mã nếu file đó đã được mã hóa từ trước, không cần mở phần mềm hay công cụ bên ngoài.

## **Mục đích & Lợi ích**
- **Bảo mật dữ liệu:** Bảo vệ các file khỏi bị truy cập trái phép bằng cách mã hóa chúng với một mật khẩu bảo mật.
- **Dễ sử dụng:** Người dùng có thể mã hóa và giải mã file trực tiếp từ menu chuột phải mà không cần mở phần mềm.
- **Tích hợp vào Windows:** Phần mềm tự động thêm các tùy chọn vào menu chuột phải của File Explorer khi được chạy lần đầu.

---

## **Cách Cài Đặt & Sử Dụng**

### **Bước 1: Cài đặt phần mềm**
1. **Tải phần mềm** từ nguồn cung cấp.
2. **Chạy `file_encryption.exe và file_dedecryption.exe` lần đầu tiên**. Phần mềm sẽ tự động đăng ký vào menu chuột phải của Windows. Bạn chỉ cần chạy phần mềm một lần duy nhất.
3. Người dùng cần đặt folder gốc ở ổ  **D:**

### **Bước 2: Mã hóa file**
1. **Chuột phải** vào file bạn muốn mã hóa.
2. Chọn **"Encrypt File"** từ menu chuột phải.
3. **Nhập mật khẩu bảo vệ** cho file.
4. File sẽ được mã hóa và lưu lại dưới dạng `.enc` (tên file gốc + `.enc`), và chỉ có thể mở lại khi nhập đúng mật khẩu. Mật khẩu sẽ được lưu vào **D:\\Encrypted** và khóa sẽ được lưu vào **D:\Key**

### **Bước 3: Giải mã file**
1. **Chuột phải** vào file mã hóa `.enc`.
2. Chọn **"Decrypt File"** từ menu chuột phải.
3. **Nhập mật khẩu** đã sử dụng khi mã hóa file.
4. File sẽ được giải mã và lưu vào thư mục **D:\\Decrypted**.

---

## **Nguyên lý Hoạt Động**

Phần mềm sử dụng phương thức **AES-256** để mã hóa và giải mã các file. Quá trình mã hóa và giải mã diễn ra theo các bước sau:

### **Mã hóa file:**
1. **Chuẩn bị file**: Phần mềm sẽ tạo một khóa AES (Advanced Encryption Standard) mới.
2. **Chia nhỏ file**: File cần mã hóa sẽ được chia thành các khối nhỏ và mã hóa từng khối bằng AES.
3. **Lưu trữ khóa**: Khóa AES sẽ được mã hóa riêng bằng một mật khẩu do người dùng nhập, giúp bảo vệ khóa mã hóa này.
4. **Lưu trữ thông tin**: Thông tin cần thiết như nonce, tag và khóa AES mã hóa sẽ được lưu vào file cùng với dữ liệu đã mã hóa.

### **Giải mã file:**
1. **Đọc file mã hóa**: Phần mềm sẽ lấy các thông tin cần thiết như nonce, tag và khóa AES đã được mã hóa từ file.
2. **Giải mã khóa AES**: Dùng mật khẩu người dùng nhập để giải mã khóa AES.
3. **Giải mã nội dung**: Sử dụng khóa AES giải mã để khôi phục dữ liệu ban đầu của file.

---

## **Các Thuật Toán Mã Hóa Được Sử Dụng**

### **1. AES (Advanced Encryption Standard)**
AES là một thuật toán mã hóa đối xứng mạnh mẽ và được sử dụng rộng rãi trong bảo mật dữ liệu. Phần mềm sử dụng **AES-256**, với khóa dài 256 bit, để mã hóa và giải mã dữ liệu.

#### **Lý do chọn AES-256**:
- **Bảo mật cao**: AES-256 là một trong các tiêu chuẩn mã hóa mạnh nhất hiện nay, được sử dụng trong các ứng dụng bảo mật quân sự và chính phủ.
- **Hiệu suất tốt**: Dù sử dụng khóa dài 256 bit, AES vẫn có hiệu suất rất cao trong việc mã hóa và giải mã dữ liệu.

### **2. SHA-256 (Secure Hash Algorithm)**
SHA-256 là một thuật toán băm mạnh, được sử dụng để tạo khóa từ mật khẩu người dùng. Thuật toán này đảm bảo rằng mỗi mật khẩu sẽ sinh ra một khóa duy nhất và không thể đảo ngược từ khóa.

#### **Lý do chọn SHA-256**:
- **Không thể đảo ngược**: SHA-256 tạo ra một giá trị băm không thể giải mã, bảo mật cho mật khẩu người dùng.
- **Khóa dài và an toàn**: SHA-256 tạo ra một giá trị băm dài 256 bit, đủ dài để tránh các cuộc tấn công tìm kiếm.

---

## **Tích Hợp vào Windows**

Phần mềm sử dụng **Windows Registry** để tự động thêm các lựa chọn vào menu chuột phải khi người dùng chạy lần đầu tiên.

- **"Encrypt File"**: Mã hóa file.
- **"Decrypt File"**: Giải mã file.

Phần mềm sử dụng một đoạn mã Python để tự động **thêm và xóa các mục trong registry** mà không cần người dùng phải làm thủ công. Sau khi đăng ký, người dùng chỉ cần chuột phải vào bất kỳ file nào để mã hóa hoặc giải mã chúng.

---

## **Cấu Trúc File**

- `file_encryption.exe`: Chương trình chính thực hiện mã hóa và giải mã file.
- `file_decryption.exe`: Chương trình phụ trợ giải mã các file đã mã hóa.
- `D:\\Decrypted`: Thư mục mặc định lưu các file giải mã.
- Các file mã hóa sẽ có phần mở rộng `.enc`.

---

## **Yêu Cầu Hệ Thống**
- **Hệ điều hành**: Windows 7/10/11.
- **Python**: Phần mềm được phát triển với Python, sử dụng các thư viện như `pycryptodome` cho mã hóa AES và `tkinter` cho giao diện người dùng.
- **Quyền Admin**: Cần quyền Admin để thực hiện thao tác đăng ký vào registry.

---

## **Lưu ý**
- **Chạy với quyền Administrator**: Để phần mềm có thể tự động đăng ký vào menu chuột phải, bạn cần **chạy `file_encryption.exe` với quyền Admin** lần đầu tiên.
- **Bảo mật mật khẩu**: Mật khẩu được dùng để mã hóa và giải mã khóa AES. Nếu mất mật khẩu, dữ liệu sẽ không thể khôi phục.
---

## **Kết luận**

Phần mềm mã hóa và giải mã file này giúp người dùng bảo vệ dữ liệu cá nhân một cách nhanh chóng, dễ dàng mà không yêu cầu kỹ năng chuyên môn. Với tính năng tích hợp trực tiếp vào **Windows File Explorer**, bạn có thể thực hiện các thao tác mã hóa và giải mã chỉ bằng một cú nhấp chuột.

Cảm ơn bạn đã sử dụng phần mềm và hy vọng nó sẽ giúp bạn bảo vệ dữ liệu một cách hiệu quả!

---
**Phát triển bởi Phạm Quang Minh**

