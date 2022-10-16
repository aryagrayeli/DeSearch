# Built with Seahorse v0.1.0
#
# Gives users their own on-chain four-function calculator!

from seahorse.prelude import *

declare_id('Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS')

class DeSearchAccount(Account):
  owner: Pubkey
  searches: Array[str,100]
  times: Array[u64,100]
  progress: u64

@instruction
def init(owner: Signer, ds_account: Empty[DeSearchAccount]):
    init_account = ds_account.init(payer = owner, seeds=["DeSearch", owner])
    init_account.owner = owner.key()
    for i in range(100):
        init_account.searches[i] = ""
        init_account.times[i] = 0
    init_account.progress = 0


@instruction
def add_searches(owner: Signer, account: DeSearchAccount, url: str, time: u64):
  assert owner.key() == account.owner, 'This is not your account!'
  account.searches[account.progress] = url
  account.times[account.progress] = time
  account.progress = (account.progress + 1) % 100
  


