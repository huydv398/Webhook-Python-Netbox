# Webhook-Python-Netbox
 Ghi chép tìm hiểu về Webhook-Python-Netbox

# python webhook

- Chuẩn bị môi trường:
    - Ubuntu 22.04

```bash
apt-get update
```

Cài đặt git, curl 

```bash
apt install wget byobu curl git byobu -y
```

```bash
apt install python3-pip -y
```

```bash
git clone https://github.com/huydv398/Webhook-Python-Netbox.git
```

```bash
cd Webhook-Python-Netbox/
```

```bash
pip install -r requirements.txt
```

```bash
$ vi main.py

# Token API của bot
bot_token = '5x5:xxx'
# ID chat của người nhận (có thể là ID của nhóm hoặc người dùng)
chat_id = '-636xxx7'
```

```bash
python3 main.py
```

1. Tạo tệp dịch vụ systemd: Tạo tệp dịch vụ mới cho tập lệnh Python của bạn. Bạn có thể thực hiện việc này bằng cách tạo một tệp **`my_webhook.service`** trong thư mục `/etc/systemd/system/`. Ví dụ: hãy tạo một tệp có tên **`my_webhook.service`**
    
    ```bash
    sudo nano /etc/systemd/system/my_webhook.service
    ```
    
    Thêm nội dung sau vào tệp  **`my_webhook.service`** thay thế `my_user` bằng tên người dùng của bạn và `/path/to/your/main.py` bằng đường dẫn đến tập lệnh Python của bạn:
    
    ```makefile
    [Unit]
    Description=My Python Script Webhook
    After=network.target
    
    [Service]
    #User=my_user 
    #Group=my_user 
    User=root
    Group=root
    WorkingDirectory=/root/Webhook-Python-Netbox/
    ExecStart=/usr/bin/python3 /root/Webhook-Python-Netbox/main.py
    #ExecStart=/usr/bin/python3**/path/to/your/main.py**
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    Alias=my_webhook.service
    ```
    
    Lưu tệp và thoát
    
2. **Reload systemd and start the service**: Sau khi tạo tệp dịch vụ, bạn cần tải lại systemd để tải cấu hình dịch vụ mới và khởi động dịch vụ:
    
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start my_webhook.service
    ```
    
3. **Enable the service to start on boot (optional)**: Nếu bạn muốn dịch vụ tự động khởi động khi hệ thống khởi động, bạn có thể kích hoạt nó:
    
    ```bash
    sudo systemctl enable my_webhook.service
    ```
    
4. **Check the status of the service**: Bạn có thể kiểm tra trạng thái dịch vụ của mình để xem nó có chạy mà không gặp lỗi hay không:
    
    ```bash
    sudo systemctl status my_webhook.service
    ```
    
    Thiết lập này sẽ tạo một dịch vụ systemd chạy tập lệnh Python của bạn dưới dạng daemon. Bạn có thể start, stop, restart, va enable/disable service bằng các sử dụng lệnh systemd(**`systemctl`**). Đảm bảo thay thế **`my_user`** và **`/path/to/your/main.py`** bằng các giá trị thích hợp cho hệ thống và tập lệnh của bạn.
    
    ```bash
    http://10.0.11.61:5000/webhook 
    ```