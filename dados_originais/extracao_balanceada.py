import pandas as pd

hospitalized_chunks = []
non_hospitalized_chunks = []
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

        non_hospitalized = chunk[chunk["HOSPITALIZ"] == 2].sample(
            n=len(hospitalized), random_state=42
        )
        non_hospitalized_chunks.append(non_hospitalized)

        print(
            f"[Chunk {chunk_count}] Lidas {len(chunk):,} linhas | Encontrados: {len(hospitalized):,} Internados e {len(non_hospitalized):,} Não Internados"
        )
        chunk_count += 1

df = pd.concat(hospitalized_chunks + non_hospitalized_chunks, ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
print(df.shape)

df.to_csv("../dados/DENGBR21_25_BALANCEADO.csv", index=False)
