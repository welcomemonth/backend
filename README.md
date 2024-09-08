

# GenPRD

## 项目描述
通过AI来自动化生成需求

## 安装指南
如何安装和配置项目。

```bash
# 克隆仓库
git clone https://github.com/welcomemonth/backend.git

# 进入项目目录
cd backend

# conda中创建一个新的环境
conda create -n genprd python=3.9
# 激活环境
conda activate genprd

# 安装依赖
pip install -r requirement.txt

# 初始化数据库
将.env.example复制为.env并修改自己postgresql数据库的信息

alembic init alembic  # 初始化alembic

# 修改alembic.ini中的sqlalchemy.url以及alembic/env.py中的target_metadata
```

```python
from app.sql.database import Base
from app.sql.models import *

target_metadata = Base.metadata
```


```bash
# 生成迁移脚本
alembic revision --autogenerate -m "Describe changes here"

# 应用迁移
alembic upgrade head
```

## 运行项目
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```



