#  📈 聲音照相管理系統(Dashboard)
本 Dashboard 為**噪音車事件管理與分析**平台，提供直覺化的資料視覺呈現，協助單位快速掌握各場域噪音事件的成效與趨勢。透過整合聲音照相設備所回傳的事件資料與車牌辨識資訊，系統可即時呈現各場域的**監測績效**、**車輛類型分布**與**違規熱點**，讓管理者更有效制定執法與改善策略。


---

## 🔧 功能特色(Indicator)

### 🔹 場域監測績效分析

顯示各監測場域在不同時段的噪音事件量、抓拍次數與檢測有效率，協助找出「績效最佳區域」與「需要改善的場域」。

### 🔹 時間趨勢與熱區判斷

以日、週、月等不同維度觀察噪音事件發生趨勢，找出最容易出現噪音車的時段，並可作為執法與資源部署依據。

### 🔹 車牌排行與車輛特徵分析

提供噪音事件中最常出現的 **前 10 名車牌排行**，以及車種分布、重複違規次數等資訊，用於掌握高風險車輛。

### 🔹 多指標監測面板

整合事件數量、有效性比率、車牌辨識成功率、場域分布等多項監測指標，提供一站式聲音照相數據分析視角。



---

## 📁 專案結構(Overview)
專案主要組成包含：
- **應用程式主程式碼**（main.py …）
- **環境依賴包**（requirements.txt）
- **環境設定檔**（如 `.env`）
- **容器化設定**（Dockerfile、docker-compose.yml）


---

## 🛠 系統需求(Requirements)
- Docker（建議 28+）
- Docker Compose（建議 v2+）
- Windows/macOS 使用者請安裝 [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
- Python 3.11

---

## 🚀 快速建置(Getting Start)

### 1. 下載專案
```bash
git clone <repo-url>
```
```bash
cd <project-folder>
```

### 2. 設定環境變數

專案需使用 `.env` 系統設定參數檔案，所有運行所需的連線資訊與服務設定皆在此檔案中進行管理。

以下為 `.env` 所需的參數格式（*不含實際值*）：

```env
DB_SERVER=<internal-db-ip>
DB_DATABASE=<db-name>
DB_UID=<db-username>
DB_PWD=<db-password>
```


### 3. 啟動方式

本專案支援兩種啟動方式，可依需求選擇：


#### 3-1. Docker運行

- 自動啟動所有服務  
- 適合開發 / 測試 / 部署 
- 可依據 `docker-compose.yml` 自動啟動所有必要服務。

**啟動服務**
```bash
docker-compose up -d --build
```

**關閉服務**

```bash
docker-compose down
```


#### 3-2. 本地運行

若你希望不透過 Docker 進行本地開發，可直接以程式原生方式啟動：

```bash
pip install -r requirements.txt
```
```bash
python main.py
```
> ⚠ 注意：本地運行需要自行準備對應語言環境與套件。

---
## 📚 文件與瀏覽器

若專案包含 API 文件，請參考：

* `/docs`
* `/swagger`
* `/redoc`

或啟動後的[預設網址](http://localhost:8501)

