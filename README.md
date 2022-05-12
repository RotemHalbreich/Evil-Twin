![evil-twin](https://user-images.githubusercontent.com/66558110/168109529-d1afbe18-5563-4a45-954e-9c43d06e2723.jpg)
# 👼 *Evil Twin Attack* 😈
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
## :pencil: *Project's Authors:*
 *Eyal Levi   -  GitHub: https://github.com/LeviEyal* | *Rotem Halbreich  -  GitHub: https://github.com/RotemHalbreich* | *Moshe Crespin  -  GitHub: https://github.com/mosheCrespin*
------------------------------------------------------|------------------------------------------------------|------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------

## :question: *About The Project:*
### *In this project we've created a program in Python which attacks a user over the internet in order to steal his login information. We've also created a defense program for protecting the user from such an attack.*


## :bar_chart: *The Project's Diagram:*
![EvilTwin](https://user-images.githubusercontent.com/66558110/168108301-7f8a238e-a617-48b8-9b9e-166647628f34.png)


## :white_check_mark: *Initialize The Project:*
### *What are the Hardware requirements?*
* *A Laptop with Linux OS*
* *Network Interface Controller (NIC) - Tenda in our case.*

*Clone the project using the Command Line by typing the command:*
`git clone https://github.com/LeviEyal/EvilTwin.git`
* *Run* `sudo install python3` *in the Command Line to download Python.*
* *Run* `sudo sh Requierments.sh` *in the Command Line to download all the requirements.*
* *Run* `sudo python3 start.py` *in the Command Line to execute the program.*

## ⚔️ *__ATTACK:__*
*Will simulate scanning of packages before they're sent to the country, and will notify their departure via message. When a package is sent, it will be stored in the Redis database service as cache. To simulate arrival of the package, the Shipment Simulator will generate a QRCode for each package, which holds all the package's information and store it in Firebase cloud storage.*

## 🛡️ *__DEFENSE:__*  
*We'll display the data from Redis' cache in the Dashboard for every package which is departed to it's destination and update that data in Real-time. The Dashboard also includes statistics such as number of packages per country district, charts and graphs of packages' size distribution per district and type of tax billing distribution per district.*




## :books: *Services used in this project:*
  *Service:* | *Logo:* | *Explanation:*
------------------------------------------------------|------------------------------------------------------|------------------------------------------------------
*__[Docker](https://www.docker.com/)__* | ![rsz_docker](https://user-images.githubusercontent.com/66558110/138525534-5b80cfff-9cc8-49d8-91ee-56dad30554ac.png) | *Docker is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers.*
*__[Redis](https://redis.io/)__* | ![rsz_1redis](https://user-images.githubusercontent.com/66558110/138525323-e48deafc-5d80-44cb-881c-543cbb9b4328.png) | *Redis (Remote Dictionary Server) is an in-memory data structure store, used as a distributed, in-memory key–value database, cache and message broker, with optional durability.*
*__[Firebase](https://firebase.google.com/)__* | ![rsz_firebase](https://user-images.githubusercontent.com/66558110/138526112-1f4f9d97-cc27-4cfa-ae9a-748839022443.png) | *Firebase is a platform developed by Google for creating mobile and web applications. Firebase has launched Cloud Firestore, a real-time document database as the successor product to the original Firebase Realtime Database.*
*__[MongoDB](https://www.mongodb.com/)__* | ![rsz_mongo](https://user-images.githubusercontent.com/66558110/138526141-b3b75e15-ca4c-4a79-b6eb-c76c935b98d8.png) | *MongoDB is a source-available cross-platform document-oriented database program. Classified as a NoSQL database program, MongoDB uses JSON-like documents with optional schemas.*
*__[BigML](https://bigml.com/)__* | ![rsz_bigml](https://user-images.githubusercontent.com/66558110/138526204-8149be8b-c540-4a35-b475-b0b94d32e375.png) | *BigML offers a highly scalable, cloud-based Machine Learning service that is easy to use, seamless to integrate, and instantly actionable. Now everyone can implement data-driven decision making in their applications. BigML works with small and big data.*
*__[Node.js](https://nodejs.org/en/)__* | ![rsz_nodejs](https://user-images.githubusercontent.com/66558110/138526220-82e94b3d-72c3-47fc-a698-2d31bfc8cb85.png) | *Node.js is an open-source, cross-platform, back-end JavaScript runtime environment that runs on the V8 engine and executes JavaScript code outside a web browser. Node.js lets developers use JavaScript to write command line tools and for server-side scripting—running scripts server-side to produce dynamic web page content before the page is sent to the user's web browser.*
*__[QRCode](https://en.wikipedia.org/wiki/QR_code)__* | ![rsz_qrcode](https://user-images.githubusercontent.com/66558110/138526484-f97cda37-1b6c-47b3-9850-ea254c390728.png) | *A QRCode (Quick Response code) is a type of matrix barcode (or two-dimensional barcode). A barcode is a machine-readable optical label that contains information about the item to which it is attached.*

# :octocat: *Enjoy, and please share!* :smile:


