docker build -t registry.cn-hangzhou.aliyuncs.com/ybase/tencent_entities:latest .
docker login -u baiyunhui@yuanben -p yb123::: registry.cn-hangzhou.aliyuncs.com
docker push registry.cn-hangzhou.aliyuncs.com/ybase/tencent_entities:latest
