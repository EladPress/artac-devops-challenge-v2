# Changelog

All notable changes to this project are documented here.
This file is maintained automatically by [semantic-release](https://github.com/semantic-release/semantic-release).

## [1.1.0](https://github.com/EladPress/artac-devops-challenge-v2/compare/v1.0.1...v1.1.0) (2026-06-08)

### Features

* Added 'ASSESSMENT.md' file that will include all changes I made ([94392fd](https://github.com/EladPress/artac-devops-challenge-v2/commit/94392fd4df10495a4ae29ce5b045085d5092e801))

### Bug Fixes

* Added .dockerignore file and modified Dockerfile to be slimmer and more efficient during building ([f809fe4](https://github.com/EladPress/artac-devops-challenge-v2/commit/f809fe4f6966c8d9dd93a8f3bbcfc42a0836a148))
* Changed Docker image healthcheck to poll /ready instead of /health ([8264b20](https://github.com/EladPress/artac-devops-challenge-v2/commit/8264b20bcc02a1fde514d37b8c8c55da1ff40149))
* Cleaning up and Adding to ASSESSMENT.md ([56ac64e](https://github.com/EladPress/artac-devops-challenge-v2/commit/56ac64e7721b48bf44e6c3bd659867f5e7bf6270))
* modified .gitignore ([b3288e4](https://github.com/EladPress/artac-devops-challenge-v2/commit/b3288e42b7e683d32b2fd7c813d70e0dac8513b7))
* Raised 'scikit-learn' version to 1.8.0 because v1.6.1 is wrong ([68e7610](https://github.com/EladPress/artac-devops-challenge-v2/commit/68e76109a30b9ab186ba4deef2dbdaf12deb839b))
* This version turns out to solve both "Run Tests" and "Security Scan" jobs in CI process sooner than I thought. ([756c74a](https://github.com/EladPress/artac-devops-challenge-v2/commit/756c74a36c1c51801cfc963a37fe3a0d38770e27))

## [1.0.1](https://github.com/EladPress/artac-devops-challenge-v2/compare/v1.0.0...v1.0.1) (2026-06-07)

### Bug Fixes

* Adding build and push stage permissions to push image ([4779b51](https://github.com/EladPress/artac-devops-challenge-v2/commit/4779b516ce3d89d1d756b4cb83d4789329c0dff4))
* For now push all images so I can test them without merging to main ([c36a722](https://github.com/EladPress/artac-devops-challenge-v2/commit/c36a72225ce78999c9795d642bf1ea3a1572e9c9))

## 1.0.0 (2026-06-07)

### Features

* FIrst commit and Added Semantic Release ([357d587](https://github.com/EladPress/artac-devops-challenge-v2/commit/357d5878ece1acbedc3ff4f808520b6beca3c9d8))

### Bug Fixes

* Lowercased image name and registry in ci.yml ([6a364e8](https://github.com/EladPress/artac-devops-challenge-v2/commit/6a364e8ff65bb0fd5f46f7efbbaf9ff6676ba0cc))
* Merged release.yml and CI.yml because it was causing headaches ([1fd1eee](https://github.com/EladPress/artac-devops-challenge-v2/commit/1fd1eeed82ac225b52fed3bc05201bf0883d3184))

<!-- New release sections are inserted below this line by semantic-release. -->
