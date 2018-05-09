Blockchain
==========
A simple blockchain system, designed for tests and studies about distributed storage and systems.
Not meant for commercial uses.

## Functionality
Each node uses REST protocols to connect with each other nodes and create the network.

## Endpoints

| Method | Endpoint     | Entry                    | Result                 |
| ------ | ------------ | -----                    | ---------------------- |
| POST   | /blockchain/ | sender, receiver, amount | Creates a transaction and returns the object created with hash and timestamp |  
| GET    | / | | Returns the whole blockchain data |
| GET | /blockchain/block/{index} | | Returns a single block by index |

