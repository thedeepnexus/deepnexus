embedding_models = [
#	STS_Average	NLI_Average	Clustering_Average	Retrieval_Average	Weighted_Average	Rank
"Alibaba-NLP/gte-Qwen2-7B-instruct-fp16", #	85.55	79.48	67.34	74.15	65.5	1
"intfloat/multilingual-e5-large-instruct", #	82.24	65.69	70.4	71.74	63.82	2
"dragonkue/snowflake-arctic-embed-l-v2.0-ko", #	81.9	60.21	63.82	78.13	63.11	3
"nlpai-lab/KURE-v1", #	83.37	64.79	61.6	75.67	62.22	4
"kakaocorp/kanana-nano-2.1b-embedding-fp16", #	83.26	66.86	59.68	75.32	61.68	5
"McGill-NLP/LLM2Vec-Meta-Llama-3-8B-Instruct-mntp-supervised-bf16", #	79.97	67.21	65.2	69.63	61.3	6
"nlpai-lab/KoE5", #	81.36	60.27	60.39	75.18	60.93	7
"BAAI/bge-multilingual-gemma2-fp16", #	83.78	76.44	58.76	70.46	60.88	8
"BAAI/bge-m3", #	83.46	65.32	58.27	73.55	60.47	9
"Snowflake/snowflake-arctic-embed-l-v2.0", #	76.89	58.95	58.94	75.56	59.93	10
"dragonkue/BGE-m3-ko", #	84.1	62.01	55.47	75.44	59.87	11
"FronyAI/frony-embed-medium-ko-v1", #	79.44	60.53	58.26	72.46	59.13	12
"facebook/drama-1b-fp16", #	80.76	61.09	51.1	70.92	56.43	13
"upskyy/bge-m3-korean", #	84.67	70.82	42.74	67.91
]

# 기출문제 기반 질의응답(STS, NLI, 인스트럭션 성능): gte-Qwen2-7B-instruct or e5-large-instruct
# 법령, 시행령, 시행규칙(긴 문장, 법령 텍스트 클러스터링/검색): snowflake-arctic-embed-l-v2.0-ko / KURE-v1