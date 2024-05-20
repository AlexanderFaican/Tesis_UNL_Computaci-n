// ignore_for_file: use_build_context_synchronously

import 'dart:convert';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:fluttertoast/fluttertoast.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: LoginScreen(),
    );
  }
}

class LoginScreen extends StatelessWidget {
  final TextEditingController usernameController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  LoginScreen({super.key});

  Future<void> loginUser(BuildContext context) async {
    final response = await http.post(
      Uri.parse('http://54.37.71.94/api/login/'),
      body: {
        'username': usernameController.text,
        'password': passwordController.text,
      },
    );

    if (response.statusCode == 200) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => HomeScreen()),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Error de autenticación'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final mediaQuery = MediaQuery.of(context);

    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 255, 255, 255),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color.fromRGBO(235, 230, 255, 1),
              Color.fromRGBO(255, 255, 255, 1),
            ],
          ),
        ),
        child: SingleChildScrollView(
          child: ConstrainedBox(
            constraints: BoxConstraints(
              minHeight: mediaQuery.size.height,
            ),
            child: Padding(
              padding: EdgeInsets.symmetric(
                vertical: mediaQuery.size.height * 0.1,
                horizontal: mediaQuery.size.width * 0.1,
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Image.asset(
                    'assets/logoNacional.png',
                    height: mediaQuery.size.height * 0.3,
                    width: mediaQuery.size.height * 0.4,
                  ),
                  const Text(
                    'Bienvenido al Monitoreo del Ganado Bovino',
                    style: TextStyle(
                      color: Color.fromARGB(255, 0, 0, 0),
                      fontSize: 16,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: mediaQuery.size.width * 0.8,
                    child: TextField(
                      controller: usernameController,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'Usuario',
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: mediaQuery.size.width * 0.8,
                    child: TextField(
                      controller: passwordController,
                      obscureText: true,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'Contraseña',
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: mediaQuery.size.width * 0.8,
                    child: ElevatedButton(
                      onPressed: () => loginUser(context),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue,
                        padding: const EdgeInsets.all(17),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(6.0),
                        ),
                      ),
                      child: const Center(
                        child: Text(
                          'Iniciar sesión',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool isMonitoring1 = false;
  bool isMonitoring2 = false;
  String monitoringMessage1 = 'Collar 1: Sin monitorear';
  String monitoringMessage2 = 'Collar 2: Sin monitorear';
  Color textColor1 = Colors.black;
  Color textColor2 = Colors.black;

  void startMonitoringSensor1(BuildContext context) async {
    await startMonitoring(context, 1);
  }

  void startMonitoringSensor2(BuildContext context) async {
    await startMonitoring(context, 2);
  }

  Future<void> startMonitoring(BuildContext context, int sensorNumber) async {
    setState(() {
      if (sensorNumber == 1) {
        isMonitoring1 = true;
        monitoringMessage1 = 'Collar 1: Cargando...';
        textColor1 = Colors.black;
      } else {
        isMonitoring2 = true;
        monitoringMessage2 = 'Collar 2: Cargando...';
        textColor2 = Colors.black;
      }
    });

    await Future.delayed(Duration(seconds: 5));

    try {
      final result = await fetchData(sensorNumber);

      final pulsaciones = result?['pulsaciones'] ?? 0;
      final temperatura = result?['temperatura'] ?? 0.0;
      final nombre_vaca = result?['nombre_vaca'] ?? 0;

      setState(() {
        if (sensorNumber == 1) {
          monitoringMessage1 =
              'Collar 1: $nombre_vaca\nTemperatura: $temperatura°C\nPulsaciones: $pulsaciones';

          if (pulsaciones >= 60 &&
              pulsaciones <= 80 &&
              temperatura >= 37.0 &&
              temperatura <= 38.0) {
            textColor1 = Colors.green;
          } else {
            textColor1 = Colors.red;

            Fluttertoast.showToast(
              msg: '¡Alerta! Signos Vitales Alterados',
              toastLength: Toast.LENGTH_LONG,
              gravity: ToastGravity.BOTTOM,
              timeInSecForIosWeb: 1,
              backgroundColor: Colors.red,
              textColor: Colors.white,
              fontSize: 16.0,
            );
          }
        } else {
          monitoringMessage2 =
              'Collar 2: $nombre_vaca\nTemperatura: $temperatura°C\nPulsaciones: $pulsaciones';

          if (pulsaciones >= 60 &&
              pulsaciones <= 80 &&
              temperatura >= 37.0 &&
              temperatura <= 38.0) {
            textColor2 = Colors.green;
          } else {
            textColor2 = Colors.red;

            Fluttertoast.showToast(
              msg: '¡Alerta! Signos Vitales Alterados',
              toastLength: Toast.LENGTH_LONG,
              gravity: ToastGravity.BOTTOM,
              timeInSecForIosWeb: 1,
              backgroundColor: Colors.red,
              textColor: Colors.white,
              fontSize: 16.0,
            );
          }
        }
      });
    } catch (error) {
      setState(() {
        if (sensorNumber == 1) {
          monitoringMessage1 =
              'Collar 1: Error al cargar los datos desde la API';
          textColor1 = Colors.red;
        } else {
          monitoringMessage2 =
              'Collar 2: Error al cargar los datos desde la API';
          textColor2 = Colors.red;
        }
      });
    } finally {
      setState(() {
        if (sensorNumber == 1) {
          isMonitoring1 = false;
        } else {
          isMonitoring2 = false;
        }
      });
    }
  }

  Future<Map<String, dynamic>?> fetchData(int sensorNumber) async {
    final response = await http.get(Uri.parse(sensorNumber == 1
        // ? 'http://192.168.1.71:8000/api/datos3/id1'
        // : 'http://192.168.1.71:8000/api/datos3/id2'));
        ? 'http://54.37.71.94/api/datos3/id1'
        : 'http://54.37.71.94/api/datos3/id2'));
    print('Respuesta de la API: ${response.body}');

    if (response.statusCode == 200) {
      return json.decode(response.body)['reportes'][0];
    } else {
      throw Exception('Error al cargar los datos desde la API');
    }
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        Navigator.of(context).popUntil((route) => route.isFirst);
        return true;
      },
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.white,
          title: Row(
            children: [
              Image.asset('assets/logoCarrera.jpeg', height: 50, width: 50),
              SizedBox(width: 8),
              Text('Panel de Monitoreo', style: TextStyle(color: Colors.black)),
            ],
          ),
          actions: [
            IconButton(
              icon: Icon(Icons.exit_to_app, color: Colors.black),
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => LoginScreen()),
                );
              },
            ),
          ],
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Card(
                color: Color.fromARGB(255, 237, 249, 255),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10.0),
                ),
                elevation: 5,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    mainAxisAlignment:
                        MainAxisAlignment.center, // Centrar verticalmente
                    crossAxisAlignment:
                        CrossAxisAlignment.center, // Centrar horizontalmente
                    children: [
                      Icon(
                        Icons.sensors,
                        color: textColor1,
                        size: 50,
                      ),
                      SizedBox(height: 10),
                      Text(
                        monitoringMessage1,
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: textColor1,
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: () => startMonitoringSensor1(context),
                icon: Icon(
                  isMonitoring1 ? Icons.hourglass_empty : Icons.play_arrow,
                  size: 30,
                ),
                label: Text(
                  isMonitoring1
                      ? 'Collar 1 (Cargando...)'
                      : 'Collar 1 (desactivado)',
                  style: TextStyle(
                    fontSize: 18,
                    color: Colors.white,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue, // Color de fondo del botón
                  padding: EdgeInsets.all(16.0),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10.0),
                  ),
                ),
              ),
              SizedBox(height: 20),
              Card(
                color: Color.fromARGB(255, 237, 249, 255),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10.0),
                ),
                elevation: 5,
                child: Padding(
                  padding: const EdgeInsets.all(12.0),
                  child: Column(
                    mainAxisAlignment:
                        MainAxisAlignment.center, // Centrar verticalmente
                    crossAxisAlignment:
                        CrossAxisAlignment.center, // Centrar horizontalmente
                    children: [
                      Icon(
                        Icons.sensors,
                        color: textColor2,
                        size: 50,
                      ),
                      SizedBox(height: 10),
                      Text(
                        monitoringMessage2,
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: textColor2,
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: () => startMonitoringSensor2(context),
                icon: Icon(
                  isMonitoring2 ? Icons.hourglass_empty : Icons.play_arrow,
                  size: 30,
                ),
                label: Text(
                  isMonitoring2
                      ? 'Collar 2 (Cargando...)'
                      : 'Collar 2 (desactivado)',
                  style: TextStyle(
                    fontSize: 18,
                    color: Colors.white,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue, // Color de fondo del botón
                  padding: EdgeInsets.all(12.0),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10.0),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
