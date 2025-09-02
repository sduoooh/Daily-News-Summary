target_path = "./.github/workflows/daily-news.yml"
temp_path = "./temp.yml"

def _renew(envs: list[str]):
    with open(temp_path, 'r') as file:
        content = file.read()
    envs_str = "\n".join([f"        {var}: ${{{{ secrets.{var} }}}}" for var in envs])
    with open(target_path, 'w') as file:
        file.write(content.replace("<env>", envs_str))

def get_envs() -> list[str]:
    import config
    return [var for var in dir(config) if var.isupper()]

if __name__ == "__main__":
    _renew(get_envs())
