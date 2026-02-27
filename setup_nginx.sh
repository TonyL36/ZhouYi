#!/bin/bash

# 1. 自动查找 Nginx 配置文件路径
NGINX_CONF=$(nginx -t 2>&1 | grep "configuration file" | awk '{print $5}')

if [ -z "$NGINX_CONF" ]; then
    echo "❌ 未找到 Nginx 配置文件，请手动配置。"
    exit 1
fi

echo "✅ 找到 Nginx 配置文件: $NGINX_CONF"

# 2. 备份原配置
cp $NGINX_CONF "$NGINX_CONF.bak_$(date +%F_%T)"
echo "✅ 已备份原配置为: $NGINX_CONF.bak_..."

# 3. 注入反向代理规则 (插入到 server 块中)
# 这里使用 sed 在 'server_name' 行之后插入我们的 location 块
# 假设 server_name 是通用的配置项

PROXY_CONFIG="
    # === ZhouYi Proxy Start ===
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
    # === ZhouYi Proxy End ===
"

# 尝试在 server_name localhost; 后插入
# 如果您的配置中不是 localhost，可能需要调整
if grep -q "server_name" $NGINX_CONF; then
    # 使用临时文件处理
    awk -v config="$PROXY_CONFIG" '/server_name/ { print; print config; next } 1' $NGINX_CONF > "${NGINX_CONF}.tmp"
    mv "${NGINX_CONF}.tmp" $NGINX_CONF
    
    # 4. 验证并重载
    nginx -t
    if [ $? -eq 0 ]; then
        nginx -s reload
        echo "🎉 配置成功！现在可以通过 http://47.109.193.180/book/ZhouYi 访问了。"
    else
        echo "❌ 配置有误，正在回滚..."
        mv "$NGINX_CONF.bak_*" $NGINX_CONF
        nginx -s reload
    fi
else
    echo "⚠️ 未找到 server_name 标记，脚本无法自动插入。请手动复制规则。"
    echo "$PROXY_CONFIG"
fi