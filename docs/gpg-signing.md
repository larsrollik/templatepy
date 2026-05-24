# GPG signing

Signing commits and tags is optional but recommended for open-source projects. GitHub shows a "Verified" badge on signed commits.

## Generate a key

```sh
gpg --full-generate-key
```

Recommended options:

- Key type: `(9) ECC (sign and encrypt)` → Curve 25519
- Expiry: `2y` (rotate every two years)
- Name and email matching your GitHub account

## Find your key ID

```sh
gpg --list-secret-keys --keyid-format LONG
```

Output:

```
sec   ed25519/<KEY_ID> 2024-01-01 [SC] [expires: 2026-01-01]
      ABCDEF1234567890ABCDEF1234567890ABCDEF12
uid   [ultimate] Your Name <you@example.com>
ssb   cv25519/<SUBKEY_ID> 2024-01-01 [E]
```

The `<KEY_ID>` is the 16-character hex string after `ed25519/`.

## Configure git to use the key

```sh
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true
git config --global tag.gpgSign true
```

## Add the public key to GitHub

```sh
gpg --armor --export <KEY_ID>
```

Copy the output (including `-----BEGIN PGP PUBLIC KEY BLOCK-----`).

Go to **GitHub → Settings → SSH and GPG keys → New GPG key** and paste it.

## Common issues

**GPG hangs and never asks for passphrase**

```sh
export GPG_TTY=$(tty)
```

Add this to your shell profile (`~/.zshrc` or `~/.bashrc`) to make it permanent.

**`error: gpg failed to sign the data`**

```sh
gpgconf --kill gpg-agent
gpg-agent --daemon
```

**Wrong key used / multiple keys**

Check which key git is using:

```sh
git config --global user.signingkey
```

List all available secret keys:

```sh
gpg --list-secret-keys
```

**Key expired**

Extend expiry without creating a new key:

```sh
gpg --edit-key <KEY_ID>
# at the gpg> prompt:
expire
# follow prompts, then:
save
# re-export and update the key on GitHub
gpg --armor --export <KEY_ID>
```

## Disabling signing temporarily

```sh
git commit --no-gpg-sign -m "message"
git tag --no-sign v1.0.0
```

Or disable globally:

```sh
git config --global commit.gpgsign false
git config --global tag.gpgSign false
```
