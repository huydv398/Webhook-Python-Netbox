# Webhook-Python-Netbox
 Ghi chép tìm hiểu về Webhook-Python-Netbox

### Python + webhook

- Chuẩn bị môi trường:
    - Ubuntu 22.04

```bash
apt-get update
```

Cài đặt git, curl 

```bash
apt install wget byobu curl git byobu -y
```

Cài đặt PIP:
```bash
apt install python3-pip -y
```

Tải Code về máy
```bash
git clone https://github.com/huydv398/Webhook-Python-Netbox.git
```
Di chuyển vào trong thư mục chưa code
```bash
cd Webhook-Python-Netbox/
```
Cài đặt các gói yêu cầu:
```bash
pip install -r requirements.txt
```
Sửa `bot_token` và `chat_id` theo thông số của bạn
```bash
$ vi main.py

# Token API của bot
bot_token = '5x5:xxx'
# ID chat của người nhận (có thể là ID của nhóm hoặc người dùng)
chat_id = '-636xxx7'
```

Chạy thử code
```bash
python3 main.py
```

Ta được kết quả sau:
```
root@webhook-receiver:~/Webhook-Python-Netbox# python3 main.py 
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.16.66.118:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 103-757-203
 ```

Thực hiện lệnh sau để test
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

**Đường dẫn dùng để khai báo để hook vào** 
```bash
http://IP_server:5000/webhook 
```

test thử một đường dẫn mà netbox sẽ sử dụng để POST tới webhook:
```
curl -X 'POST' 'http://172.16.66.118:5000/webhook ' -H 'connection: close' -H 'x-hook-signature: 58eb118ae1f95a3b2a8c4ef309f83d4ad2c2efa0a4142b51560d9bd58c199e1bc2520103402ff15a226994b76189b0c1eacfe0f106077cb2d041bb97383819ad' -H 'content-length: 1057' -H 'content-type: application/json' -H 'user-agent: python-urllib3/2.2.1' -H 'accept-encoding: identity' -H 'host: webhook.site' -d $'{"event": "deleted", "timestamp": "2024-05-23T04:31:17.974359+00:00", "model": "ipaddress", "username": "admin", "request_id": "15e41292-9864-49aa-bb5d-f315432a98ef", "data": {"id": 12, "url": "/api/ipam/ip-addresses/12/", "display": "103.154.63.56/24", "family": {"value": 4, "label": "IPv4"}, "address": "103.154.63.56/24", "vrf": null, "tenant": null, "status": {"value": "active", "label": "Active"}, "role": null, "assigned_object_type": null, "assigned_object_id": null, "assigned_object": null, "nat_inside": null, "nat_outside": [], "dns_name": "", "description": "", "comments": "", "tags": [], "custom_fields": {}, "created": "2024-05-23T04:31:02.114908Z", "last_updated": "2024-05-23T04:31:02.114940Z"}, "snapshots": {"prechange": {"created": "2024-05-23T04:31:02.114Z", "description": "", "comments": "", "address": "103.154.63.56/24", "vrf": null, "tenant": null, "status": "active", "role": "", "assigned_object_type": null, "assigned_object_id": null, "nat_inside": null, "dns_name": "", "custom_fields": {}, "tags": []}, "postchange": null}}'
```

Kết quả trả về như sau:
![Imgur](https://imgur.com/72qytQh)

