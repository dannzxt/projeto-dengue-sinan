import pandas as pd

hospitalized_chunks = []
non_hospitalized_chunks = []
total_hospitalized = 0
total = 0
test_percent = 0.2
hospitalized_test_percent = 0.032190922355718  # proporção real dos dados


def calculate_prop_non_hospitalized(test_percent, hospitalized_test_percent):
    train_percent = 1 - test_percent
    non_hospitalized_test_percent = 1 - hospitalized_test_percent

    coef_hospitalized = hospitalized_test_percent * test_percent + 0.5 * train_percent
    coef_non_hospitalized = (
        non_hospitalized_test_percent * test_percent + 0.5 * train_percent
    )

    return coef_non_hospitalized / coef_hospitalized


for year in [21, 22, 23, 24, 25]:
    chunk_size = 100000
    chunk_count = 1

    print("-" * 60)
    print(f"📂 INICIANDO EXTRAÇÃO: Base DENGBR20{year}.csv")
    print("-" * 60)

    for chunk in pd.read_csv(
        f"DENGBR{year}.csv", chunksize=chunk_size, low_memory=False
    ):
        hospitalized = chunk[chunk["HOSPITALIZ"] == 1]
        hospitalized_chunks.append(hospitalized)

        total_hospitalized += len(hospitalized)
        total += len(chunk)

        num_non_hospitalized = int(
            calculate_prop_non_hospitalized(test_percent, hospitalized_test_percent)
            * len(hospitalized)
        )
        non_hospitalized = chunk[chunk["HOSPITALIZ"] == 2].sample(
            n=int(num_non_hospitalized), random_state=42
        )
        non_hospitalized_chunks.append(non_hospitalized)

        print(
            f"[Chunk {chunk_count}] Lidas {len(chunk):,} linhas | Encontrados: {len(hospitalized):,} Internados e {len(non_hospitalized):,} Não Internados"
        )
        chunk_count += 1

df = pd.concat(hospitalized_chunks + non_hospitalized_chunks, ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
print(df.shape)
print(total_hospitalized / total)

df.to_csv("../dados/DENGBR21_25_BALANCEADO.csv", index=False)
