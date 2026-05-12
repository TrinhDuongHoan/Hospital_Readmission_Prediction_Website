diabetes-mlops-streaming/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
│
├── docs/
│   ├── architecture/
│   ├── diagrams/
│   ├── report/
│   └── api/
│
├── configs/
│   ├── app.yaml
│   ├── kafka.yaml
│   ├── spark.yaml
│   └── model.yaml
│
├── data/
│   ├── raw/
│   │   └── diabetic_data.csv
│   ├── sample/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_experiments.ipynb
│
├── src/
│   ├── common/
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── constants.py
│   │   └── utils.py
│   │
│   ├── ingestion/
│   │   ├── load_data.py
│   │   ├── validate_data.py
│   │   └── publish_events.py
│   │
│   ├── simulator/
│   │   ├── event_builder.py
│   │   ├── producer.py
│   │   └── run_simulator.py
│   │
│   ├── streaming/
│   │   ├── spark_job.py
│   │   ├── transforms.py
│   │   ├── features_online.py
│   │   └── sinks.py
│   │
│   ├── features/
│   │   ├── feature_store.py
│   │   ├── build_offline_features.py
│   │   └── mappings.py
│   │
│   ├── training/
│   │   ├── preprocess.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── predict_batch.py
│   │
│   ├── inference/
│   │   ├── predictor.py
│   │   ├── model_loader.py
│   │   └── postprocess.py
│   │
│   ├── api/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── routes.py
│   │
│   └── monitoring/
│       ├── service_metrics.py
│       ├── drift_report.py
│       └── feedback_loop.py
│
├── tests/
│   ├── test_preprocess.py
│   ├── test_train.py
│   ├── test_api.py
│   └── test_streaming.py
│
├── scripts/
│   ├── setup_local.sh
│   ├── run_train.sh
│   ├── run_api.sh
│   ├── run_simulator.sh
│   └── create_topics.sh
│
├── artifacts/
│   ├── models/
│   ├── metrics/
│   └── logs/
│
└── ui/
    └── mockups/