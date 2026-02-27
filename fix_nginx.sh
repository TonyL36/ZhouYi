#!/bin/bash
TARGET="/etc/nginx/sites-enabled/familysys-frontend"

# 1. 备份
cp $TARGET ${TARGET}.bak_$(date +%s)

# 2. 删除之前可能错误添加的 ZhouYi 配置块 (如果存在)
sed -i '/location \/book\/ZhouYi/,/location \/images/d' $TARGET

# 3. 去掉文件末尾的 "}"
sed -i '$d' $TARGET

# 4. 追加新配置
cat >> $TARGET <<EOF

    # === ZhouYi Proxy ===
    location /book/ZhouYi {
        proxy_pass http://127.0.0.1:6400/book/ZhouYi;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /api {
        proxy_pass http://127.0.0.1:6401/api;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /images {
        proxy_pass http://127.0.0.1:6401/images;
    }
}
EOF

# 5. 重载
nginx -t && nginx -s reload
echo "Config Updated!"
