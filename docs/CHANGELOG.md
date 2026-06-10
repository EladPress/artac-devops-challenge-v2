# Changelog

All notable changes to this project are documented here.
This file is maintained automatically by [semantic-release](https://github.com/semantic-release/semantic-release).

## [1.2.1](https://github.com/EladPress/artac-devops-challenge-v2/compare/v1.2.0...v1.2.1) (2026-06-10)

### Bug Fixes

* Add encryption for the root block device and downsized to 10GB ([36cea3b](https://github.com/EladPress/artac-devops-challenge-v2/commit/36cea3b4e7d3106eac3a185f026ca19afa3e43b9))
* changed app_url output in Terraform to public dns ([1b4dfd0](https://github.com/EladPress/artac-devops-challenge-v2/commit/1b4dfd0e478cbbebae0892fdbde44430e86b9d23))
* Fixed "Delete image artifact" step deleting artifacts from other builds ([de33ecf](https://github.com/EladPress/artac-devops-challenge-v2/commit/de33ecfd06d966b6b9b0711b4f6cb31db5d27198))
* Fixed deploying on other regions because of a hardcoded AMI ID ([91c46d4](https://github.com/EladPress/artac-devops-challenge-v2/commit/91c46d4df78c0e4461d40d5ae49ce321df3764d5))
* Validated Terraform implementation. Moved to using SSM instead of SSH. Made it possible to switch regions. ([bdaf4aa](https://github.com/EladPress/artac-devops-challenge-v2/commit/bdaf4aa854d0df0b9817346393f9b681b5e82c2e))

## [1.2.0](https://github.com/EladPress/artac-devops-challenge-v2/compare/v1.1.0...v1.2.0) (2026-06-09)

### Features

* Changed image naming convention to branch_name-build_increment and semantic versioning for release/prerelease versions ([83b726b](https://github.com/EladPress/artac-devops-challenge-v2/commit/83b726b911bc0f240178e0487b1c3059d5e49c5c))
* images built and push now will have a tag of the new version if exists, and the branch and build number ([6bd3958](https://github.com/EladPress/artac-devops-challenge-v2/commit/6bd3958a2bbc98d2e217160b3958d8347de3f36a))

### Bug Fixes

* Added a smoke test in CI process ([855dd59](https://github.com/EladPress/artac-devops-challenge-v2/commit/855dd597e9f5e1bf244ab2a8dcdc31687a5063e4))
* Added artifact cleanup after they are not in use in ci.yml ([f6a7dd8](https://github.com/EladPress/artac-devops-challenge-v2/commit/f6a7dd85c1663468dcc10c0bba4b2e8fbe246c70))
* Added dependabot to update actions that are about to be deprecated ([359471d](https://github.com/EladPress/artac-devops-challenge-v2/commit/359471d241e47dd22ffbdabcd1e8a632a4e2528b))
* CI will now only push the Docker image after all tests and scans are done to prevent a flawed image from being pushed ([258fe1a](https://github.com/EladPress/artac-devops-challenge-v2/commit/258fe1a471f208e6a6d1897db7cbd9d7b2dc2e2a))
* Divided Trivy scan so all types of vulnerabilites are reported but only HIGH and CRITICAL fail the build ([c48a38a](https://github.com/EladPress/artac-devops-challenge-v2/commit/c48a38aa3e614729beb1d1435fa215f3070cce7d))
* Locking Trivy version in ci.yml ([c1dc8fe](https://github.com/EladPress/artac-devops-challenge-v2/commit/c1dc8fe7c1a61d874dc02e84884cb41214c0607a))
* Removed Semantic Release preview for now to allow proper image tagging only on release branches ([d426d3b](https://github.com/EladPress/artac-devops-challenge-v2/commit/d426d3bef1eec4eba03af9798d4f90894ab9f4b5))
* Updated actions version because of Node20 becoming deprecated ([84da2d2](https://github.com/EladPress/artac-devops-challenge-v2/commit/84da2d276313a1391a8f3b6c179e0a94c3620e3d))
* Upgraded to a higher fastapi version to fix HIGH vulnerability with its dependency, 'starlette' ([4bf4d96](https://github.com/EladPress/artac-devops-challenge-v2/commit/4bf4d964799c1fb8f333e211dd593860d6670dfe))

## [1.2.0-dev.1](https://github.com/EladPress/artac-devops-challenge-v2/compare/v1.1.0...v1.2.0-dev.1) (2026-06-09)

### Features

* Changed image naming convention to branch_name-build_increment and semantic versioning for release/prerelease versions ([83b726b](https://github.com/EladPress/artac-devops-challenge-v2/commit/83b726b911bc0f240178e0487b1c3059d5e49c5c))
* images built and push now will have a tag of the new version if exists, and the branch and build number ([6bd3958](https://github.com/EladPress/artac-devops-challenge-v2/commit/6bd3958a2bbc98d2e217160b3958d8347de3f36a))

### Bug Fixes

* Added a smoke test in CI process ([855dd59](https://github.com/EladPress/artac-devops-challenge-v2/commit/855dd597e9f5e1bf244ab2a8dcdc31687a5063e4))
* Added artifact cleanup after they are not in use in ci.yml ([f6a7dd8](https://github.com/EladPress/artac-devops-challenge-v2/commit/f6a7dd85c1663468dcc10c0bba4b2e8fbe246c70))
* Added dependabot to update actions that are about to be deprecated ([359471d](https://github.com/EladPress/artac-devops-challenge-v2/commit/359471d241e47dd22ffbdabcd1e8a632a4e2528b))
* CI will now only push the Docker image after all tests and scans are done to prevent a flawed image from being pushed ([258fe1a](https://github.com/EladPress/artac-devops-challenge-v2/commit/258fe1a471f208e6a6d1897db7cbd9d7b2dc2e2a))
* Divided Trivy scan so all types of vulnerabilites are reported but only HIGH and CRITICAL fail the build ([c48a38a](https://github.com/EladPress/artac-devops-challenge-v2/commit/c48a38aa3e614729beb1d1435fa215f3070cce7d))
* Locking Trivy version in ci.yml ([c1dc8fe](https://github.com/EladPress/artac-devops-challenge-v2/commit/c1dc8fe7c1a61d874dc02e84884cb41214c0607a))
* Removed Semantic Release preview for now to allow proper image tagging only on release branches ([d426d3b](https://github.com/EladPress/artac-devops-challenge-v2/commit/d426d3bef1eec4eba03af9798d4f90894ab9f4b5))
* Updated actions version because of Node20 becoming deprecated ([84da2d2](https://github.com/EladPress/artac-devops-challenge-v2/commit/84da2d276313a1391a8f3b6c179e0a94c3620e3d))
* Upgraded to a higher fastapi version to fix HIGH vulnerability with its dependency, 'starlette' ([4bf4d96](https://github.com/EladPress/artac-devops-challenge-v2/commit/4bf4d964799c1fb8f333e211dd593860d6670dfe))

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
