import tensorflow as tf
import pickle
import numpy as np
import pandas as pd


def model_predict(form, type):
    if type == "nutrition":
        soilColor = form["soilColor"]
        nitrogen = int(form["nitrogen"])
        phosphorous = int(form["phosphorous"])
        potassium = int(form["potassium"])
        pH = float(form["pH"])
        rainfall = float(form["rainfall"])
        temperature = float(form["temperature"])

        # model prediction
        model = tf.keras.models.load_model("models/crop-model.h5")

        with open("models/labels/crop_txt", "rb") as f:
            crop_label = pickle.load(f)

        with open("models/fertilizers-model", "rb") as f:
            fertilizer_label = pickle.load(f)

        with open("models/labels/soil_color_txt", "rb") as f:
            soil_color_label = pickle.load(f)

        for key, value in soil_color_label.items():
            if value == soilColor:
                soilColor = key
                break

        prediction = model.predict(
            np.array(
                [
                    [
                        soilColor,
                        nitrogen,
                        phosphorous,
                        potassium,
                        pH,
                        rainfall,
                        temperature,
                    ]
                ]
            )
        )

        crop = crop_label[int(tf.argmax(prediction[0]))]
        fertilizer = fertilizer_label[crop]
        return {"crop": crop, "fertilizer": fertilizer},form

    if type == "weather":
        N = int(form["N"])
        P = int(form["P"])
        K = int(form["K"])
        temperature = float(form["temp"])
        humidity = float(form["humidity"])
        ph = float(form["pH"])
        rainfall = float(form["rainfall"])

        # model prediction
        with open("models/labels/weather_crop_labels", "rb") as f:
            weather_crop_label = pickle.load(f)

        # model prediction
        model = tf.keras.models.load_model("models/crop-nutrients-model.h5")

        prediction = model.predict(
            np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        )

        weather_crop = weather_crop_label[int(tf.argmax(prediction[0]))]
        return {"weather_crop": weather_crop},form

    if type == "fruits":
        N = int(form["N"])
        P = int(form["P"])
        K = int(form["K"])
        pH = float(form["pH"])
        EC = float(form["EC"])
        S = float(form["S"])
        Cu = float(form["Cu"])
        Fe = float(form["Fe"])
        Mn = float(form["Mn"])
        B = float(form["B"])
        Zn = float(form["Zn"])
        # model prediction

        with open("models/labels/fruits_txt", "rb") as f:
            fruit_label = pickle.load(f)

        # model prediction
        model = tf.keras.models.load_model("models/fruits_model.h5")

        prediction = model.predict(np.array([[N, P, K, pH, EC, S, Cu, Fe, Mn, Zn, B]]))

        fruit = fruit_label[int(tf.argmax(prediction[0]))]
        return {"fruit": fruit},form


def optimization(type, details, form,time):
    if time>12:
        return details,time
    if type == "nutrition":
        print("Time: ",time)
        data = pd.read_csv("datasets/optimization/Crop and fertilizer dataset percent.csv")
        time += int(data.loc[data["Crop"]==details[-1]["crop"]]["Time to Yield"].values[0])
        soilColor = form["soilColor"]
        nitrogen = int(form["nitrogen"])*int(data.loc[data["Crop"]==details[-1]["crop"]]["Nitrogen"].values[0])
        phosphorous = int(form["phosphorous"])*int(data.loc[data["Crop"]==details[-1]["crop"]]["Phosphorus"].values[0])
        potassium = int(form["potassium"])*int(data.loc[data["Crop"]==details[-1]["crop"]][ "Potassium"].values[0])
        pH = float(form["pH"])*float(data.loc[data["Crop"]==details[-1]["crop"]]["pH"].values[0])
        rainfall = float(form["rainfall"])*float(data.loc[data["Crop"]==details[-1]["crop"]]["Rainfall"].values[0])
        temperature = float(form["temperature"])*float(data.loc[data["Crop"]==details[-1]["crop"]]["Temperature"].values[0])
        
        form = {"soilColor":soilColor,"nitrogen":nitrogen,"phosphorous":phosphorous,"potassium":potassium,"pH":pH,"rainfall":rainfall,"temperature":temperature}
        data,form = model_predict(form,type)
        details.append((data))
        return optimization(type,details,form,time),time
        
    if type == "weather":
        data = pd.read_csv("datasets/optimization/Crop_recommendation percent.csv")
        print("")
        print(details[-1]["weather_crop"])
        time += int(data.loc[data["crop"]==details[-1]["weather_crop"]]["Time to Yield"].values[0])
        N = int(form["N"])*int(data.loc[data["crop"]==details[-1]["weather_crop"]]["N"].values[0])
        P = int(form["P"])*int(data.loc[data["crop"]==details[-1]["weather_crop"]]["P"].values[0])
        K = int(form["K"])*int(data.loc[data["crop"]==details[-1]["weather_crop"]]["K"].values[0])
        temperature = float(form["temp"])
        humidity = float(form["humidity"])
        ph = float(form["pH"])
        rainfall = float(form["rainfall"])
        
        form = {"N":N,"P":P,"K":K,"temp":temperature,"humidity":humidity,"pH":ph,"rainfall":rainfall}
        data,form = model_predict(form,type)
        details.append((data))
        return optimization(type,details,form,time),time
    
    if type == "fruits":
        data = pd.read_csv("datasets/optimization/dataset percent.csv")
        print(details[-1]["fruit"])
        print("Time: ",data.loc[data["Crop"]==details[-1]["fruit"]])
        time += int(data.loc[data["Crop"]==details[-1]["fruit"]]["Time to Yield"].values[0])

        N = int(form["N"])*int(data.loc[data["Crop"]==details[-1]["fruit"]]["N"].values[0])
        P = int(form["P"])*int(data.loc[data["Crop"]==details[-1]["fruit"]]["P"].values[0])
        K = int(form["K"])*int(data.loc[data["Crop"]==details[-1]["fruit"]]["K"].values[0])
        pH = float(form["pH"])*float(data.loc[data["Crop"]==details[-1]["fruit"]]["pH"].values[0])
        EC = float(form["EC"])*float(data.loc[data["Crop"]==details[-1]["fruit"]]["EC"].values[0])
        S = float(form["S"])*float(data.loc[data["Crop"]==details[-1]["fruit"]]["S"].values[0])
        Cu = float(form["Cu"])*float(data.loc[data["Crop"]==details[-1]["fruit"]]["Cu"].values[0])
        Fe = float(form["Fe"])*float(data.loc[data["Crop"]==details[-1]["fruit"]]["Fe"].values[0])
        Mn = float(form["Mn"])*float(data.loc[data["Crop"]==details[-1]["fruit"]]["Mn"].values[0])
        B = float(form["B"])*float(data.loc[data["Crop"]==details[-1]["fruit"]]["B"].values[0])
        Zn = float(form["Zn"])*float(data.loc[data["Crop"]==details[-1]["fruit"]]["Zn"].values[0])

        form = {"N":N,"P":P,"K":K,"pH":pH,"EC":EC,"S":S,"Cu":Cu,"Fe":Fe,"Mn":Mn,"B":B,"Zn":Zn}
        data,form = model_predict(form,type)
        details.append((data))
        return optimization(type,details,form,time),time
    
