最开始用git提交是看这个文档：https://jasonai.me/blog/obsidian-git-sync/
能进行提交和同步上传。

下面具体了解每一步是干嘛的：
Git 的核心思想是**分布式版本控制**：你的本地项目本身就是一个完整的数据库，而远端（如 GitHub/GitLab）则是全员同步的主服务器。

这里用最直接的方式，逐一拆解这 6 个核心命令的使用场景与背后逻辑：

## 1. 克隆代码库：`git clone`

将远程仓库完整地下载（复制）到本地，包括代码文件、分支以及所有的历史提交记录。

- **典型使用场景**：加入新项目、或者把别人的开源项目下载到自己电脑上。
    
- **常用命令**：
    
    Bash
    
    ```
    # 克隆指定仓库（默认在当前目录下生成一个项目同名文件夹）
    git clone https://github.com/username/repository.git
    
    # 克隆并自定义本地文件夹名称
    git clone https://github.com/username/repository.git my-project
    ```
    

## 2. 保存本地快照：`git commit`

将你放在“暂存区”（Staging Area，即通过 `git add` 收集的修改）的代码变动，打包生成一个永久的历史版本（提交记录）。

- **关键概念**：Commit 仅仅发生在**本地**，不会同步到远程仓库。它就像在游戏中“存档”。
    
- **常用流程**：
    
    Bash
    
    ```
    # 1. 把修改过的文件加入暂存区（暂存所有改动）
    git add .
    
    # 2. 提交暂存区内容，并附带清晰的改动说明
    git commit -m "feat: 新增用户登录功能"
    ```
    

## 3. 推送至远程：`git push`

把你在本地 commit 的历史提交记录，上传同步到远程仓库（如 GitHub）。

- **典型使用场景**：完成一段功能开发后，把代码上传给团队其他人查看或合入主干。
    
- **常用命令**：
    
    Bash
    
    ```
    # 将本地当前的 main 分支推送到远程 origin 仓库
    git push origin main
    
    # 如果是第一次推送新建的本地分支，需要建立远程追踪关系
    git push -u origin feature-login
    ```
    

## 4. 拉取并合并：`git pull`

从远程仓库下载最新的代码改动，并**自动合并**到你当前的本地分支中。

- **关键原理**：`git pull` 实际上是两个操作的合体：**`git fetch`**（从远程下载最新变动）+ **`git merge`**（将远程变动合并入本地）。
    
- **常用命令**：
    
    Bash
    
    ```
    # 拉取远程 origin 仓库当前分支的最新代码并合并
    git pull origin main
    ```
    
    > **提示**：如果本地有未 commit 的改动，拉取前最好先 commit 或使用 `git stash` 暂存，避免文件冲突。
    

## 5. 管理分支：`git branch`

分支就像是从主线拆分出的平行宇宙，让你在不影响主线代码（如 `main` 或 `master`）的前提下，独立开发新功能或修复 Bug。

- **常用操作**：
    
    Bash
    
    ```
    # 查看本地所有分支（带 * 号的为当前所在分支）
    git branch
    
    # 创建新分支（但仍留在当前分支）
    git branch feature-user-profile
    
    # 切换到新分支
    git checkout feature-user-profile
    # 或使用较新的切换命令：
    git switch feature-user-profile
    
    # 【一步到位】创建并直接切换到新分支
    git checkout -b feature-user-profile
    # 或：
    git switch -c feature-user-profile
    
    # 删除分支（完成合并后使用）
    git branch -d feature-user-profile
    ```
    

## 6. 合并分支：`git merge`

把一个分支的修改内容和历史记录，整合到另一个分支中。

- **典型应用场景**：在 `feature-login` 分支开发完登录功能后，将其合并回主分支 `main`。
    
- **常用流程**：
    
    Bash
    
    ```
    # 1. 切换回需要接收修改的目标分支（例如 main）
    git switch main
    
    # 2. 将 feature-login 分支的修改合并进来
    git merge feature-login
    ```
    
- **注意点**：如果两个人修改了同一个文件的同一行代码，合并时会触发**冲突（Conflict）**。Git 会停止合并，需要你手动编辑冲突文件、保存后重新 `git add` 并 `git commit` 来完成合并。
    

## 一图梳理：日常标准开发工作流

Plaintext

```
[远程仓库] <------- git push ------- [本地仓库] <------- git commit ------- [暂存区] <------- git add ------- [工作区]
          -------- git pull ------> [本地仓库]
```

1. **新建分支**：`git switch -c feat/my-task`
    
2. **修改文件后暂存**：`git add .`
    
3. **提交到本地**：`git commit -m "完成需求"`
    
4. **拉取远程最新避免冲突**：`git pull origin main`
    
5. **推送到远程**：`git push origin feat/my-task`
    
6. **请求合并**：在 GitHub/GitLab 上发起 PR/MR 将分支 **merge** 到主干。