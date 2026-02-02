with open("flash_models_list.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        print(f"LEN: {len(line.strip())} VAL: {line.strip()}")
