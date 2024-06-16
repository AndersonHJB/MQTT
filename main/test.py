import bcrypt


# 加密密码
def hash_password(password):
    # 生成盐值
    salt = bcrypt.gensalt()
    # 生成哈希值
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


# 验证密码
def check_password(hashed, password):
    # 验证密码
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


# 示例使用
if __name__ == "__main__":
    password = "my_secure_password"
    hashed_password = hash_password(password)
    print(f"Hashed password: {hashed_password}")

    # 验证密码
    is_correct = check_password(hashed_password, "my_secur1e_password")
    print(f"Password is correct: {is_correct}")
