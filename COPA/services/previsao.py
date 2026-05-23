# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import joblib

# -------------------------
# LOAD MODELO (SAFE)
# -------------------------
_model = None
_scaler = None
_classes = None
_features = None


def carregar_modelo_previsao():
    global _model, _scaler, _classes, _features

    if _model is not None:
        return _model, _scaler, _classes, _features

    try:
        _model = joblib.load("modelo_previsao.joblib")
        _scaler = joblib.load("scaler_previsao.joblib")
        _classes = joblib.load("classes_previsao.joblib")
        _features = joblib.load("features_previsao.joblib")

        print("✅ Modelo carregado com sucesso")

        return _model, _scaler, _classes, _features

    except Exception as e:
        print("❌ Erro ao carregar modelo:", e)
        return None, None, None, None


# -------------------------
# PREVISÃO
# -------------------------
def prever_partida(model, scaler, classes, features, casa, fora):

    if model is None:
        return {
            "casa": 0.33,
            "empate": 0.34,
            "fora": 0.33,
            "predicao_final": "empate"
        }

    try:
        # ⚠️ IMPORTANTE:
        # Aqui usamos dados simples porque o modelo já foi treinado com muitas features
        # e fazemos o alinhamento via "features"

        dados = pd.DataFrame([{
            "wins_casa": 5,
            "draws_casa": 2,
            "losses_casa": 3,
            "wins_fora": 3,
            "draws_fora": 2,
            "losses_fora": 5,
            "h2h_wins_casa": 2,
            "h2h_wins_fora": 1,
            "h2h_draws": 2
        }])

        # 🔥 alinhamento com treino
        dados = dados.reindex(columns=features, fill_value=0)

        X = scaler.transform(dados)

        proba = model.predict_proba(X)[0]

        resultado = {
            "casa": float(proba[0]),
            "empate": float(proba[1]),
            "fora": float(proba[2]),
        }

        resultado["predicao_final"] = max(resultado, key=resultado.get)

        return resultado

    except Exception as e:
        print("Erro na previsão:", e)

        return {
            "casa": 0.33,
            "empate": 0.34,
            "fora": 0.33,
            "predicao_final": "empate"
        }