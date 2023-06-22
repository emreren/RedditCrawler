
# Reddit Crawler

Brandefense 2023 Staj Kampı Teknik Ön Eleme Projesi

Projenin çalıştırılması için aşağıdaki önkoşulların yerine getirilmiş olması gerekmektedir:

- Docker yüklü olmalıdır.

### Kurulum

1. Projeyi yerel makinenize klonlayın:

   ```bash
   git clone https://github.com/emreren/RedditCrawler.git
   ```
2. Proje dizinine geçin:

   ```bash
   cd RedditCrawler
   ```
3. Proje değişkenlerini düzenleyin:

    https://www.reddit.com/prefs/apps adresinden yeni bir script app oluşturun. `client_id`, `client_secret` ve `user_agent` değerlerini kod üzerinden değiştirin.
   ```bash
   nano crawler.py
   ```   
4. Docker imajını oluşturun:

   ```bash
   docker build -t reddit-crawler .
   ```
5. Docker konteynerini çalıştırın:

   ```bash
   docker run -d -p 8000:8000 reddit-crawler
   ```
   Uygulama, http://localhost:8000 adresinde çalışacaktır.


### Kullanım
Uygulamayı çalıştırdıktan sonra, API'ye istekler göndererek projenin sağladığı özellikleri kullanabilirsiniz.

API Dokümantasyonu: http://localhost:8000/docs