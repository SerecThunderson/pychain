
# pyChain
A lightweight self-custodial p2p ledger consensus protocol

## Intended Features    
- Verifiable ledger of transactions and blocks in a chain of hashes
- Secure private/public key system
- Self-custodial initiation of new chains
- Proof of Authoritarian Democracy system
- Block pruning, with merkle-root compressed offchain proofs
- Custom hooks 

## Telegram Core
Telegram Core stands as the inception of the project, and current workspace. It allows for a number of novel features and proof of concepts, and will be updated to further align with pyChain.
Telegram core has the following features:
- Python Telegram bot watches for valid json snippets
- Json sinppets are formatted and pushed to blocks in batches of 30
- Blocks are hashed in series, and pushed to ledger channel + ledger backup
- Ledger backup files are split every 5k blocks, pushing to channel and local storage
- Transaction messaging tied to ID
- Verifiable chain of inputs

## Support  
A star or follow helps a lot, and so does sharing with anybody who might find these resources useful. That way I can keylog them.

Donations may be made out to [SEREC.ETH](https://app.ens.domains/serec.eth), or ```0x75365dDb02bc316748fB9A2dc5a33B42f1fBA2E7```

Job offers and references are also **greatly unappreciated**. Your job sucks and cannot afford me.

If you have any questions, feel free to reach out to me on [Twitter](https://twitter.com/SerecThunderson) or [Telegram](https://t.me/SerecThunderson) after you've exhausted google and chatGPT.
        
 ## Author
#### Serec Thunderson
- Twitter: [@SerecThunderson](https://twitter.com/SerecThunderson)
- Telegram: [@SerecThunderson](https://t.me/SerecThunderson)
- Github: [@SerecThunderson](https://github.com/SerecThunderson)

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
