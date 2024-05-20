import 'dart:convert';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:fluttertoast/fluttertoast.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:fluttertoast/fluttertoast.dart';

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

  Future<void> loginUser(BuildContext context) async {
    final response = await http.post(
      Uri.parse('http://192.168.1.71:8000/api/login/'),
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
        SnackBar(
          content: Text('Error de autenticación'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Logo en el centro del login
            Image.asset('assets/logoNacional.png', height: 300, width: 300),
            SizedBox(height: 20),
            TextField(
              controller: usernameController,
              decoration: InputDecoration(labelText: 'Usuario'),
            ),
            TextField(
              controller: passwordController,
              obscureText: true,
              decoration: InputDecoration(labelText: 'Contraseña'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => loginUser(context),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.all(16.0),
              ),
              child: Text(
                'Iniciar sesión',
                style: TextStyle(fontSize: 25.0),
              ),
            ),
          ],
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
  String monitoringMessage1 = 'Sensor 1: Sin monitorear';
  String monitoringMessage2 = 'Sensor 2: Sin monitorear';
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
        monitoringMessage1 = 'Sensor 1: Cargando...';
        textColor1 = Colors.black;
      } else {
        isMonitoring2 = true;
        monitoringMessage2 = 'Sensor 2: Cargando...';
        textColor2 = Colors.black;
      }
    });

    await Future.delayed(Duration(seconds: 5));

    try {
      final result = await fetchData(sensorNumber);

      final pulsaciones = result?['pulsaciones'] ?? 0;
      final temperatura = result?['temperatura'] ?? 0.0;
      final collarId = result?['collar_id'];

      if (collarId == "1" || collarId == "2") {
        setState(() {
          if (sensorNumber == 1) {
            monitoringMessage1 = 'Sensor 1: Temperatura: $temperatura°C\n'
                'Pulsaciones: $pulsaciones';

            if (pulsaciones >= 60 &&
                pulsaciones <= 80 &&
                temperatura >= 37.0 &&
                temperatura <= 38.0) {
              textColor1 = Colors.green;
            } else {
              textColor1 = Colors.red;

              Fluttertoast.showToast(
                msg:
                    '¡Alerta! Pulsaciones o temperatura fuera del rango normal',
                toastLength: Toast.LENGTH_LONG,
                gravity: ToastGravity.BOTTOM,
                timeInSecForIosWeb: 1,
                backgroundColor: Colors.red,
                textColor: Colors.white,
                fontSize: 16.0,
              );
            }
          } else {
            monitoringMessage2 = 'Sensor 2: Temperatura: $temperatura°C\n'
                'Pulsaciones: $pulsaciones';

            if (pulsaciones >= 60 &&
                pulsaciones <= 80 &&
                temperatura >= 37.0 &&
                temperatura <= 38.0) {
              textColor2 = Colors.green;
            } else {
              textColor2 = Colors.red;

              Fluttertoast.showToast(
                msg:
                    '¡Alerta! Pulsaciones o temperatura fuera del rango normal',
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
      } else {
        setState(() {
          if (sensorNumber == 1) {
            monitoringMessage1 =
                'Sensor 1: Datos no disponibles para collar_id 1 y 2';
            textColor1 = Colors.red;
          } else {
            monitoringMessage2 =
                'Sensor 2: Datos no disponibles para collar_id 1 y 2';
            textColor2 = Colors.red;
          }
        });
      }
    } catch (error) {
      setState(() {
        if (sensorNumber == 1) {
          monitoringMessage1 =
              'Sensor 1: Error al cargar los datos desde la API';
          textColor1 = Colors.red;
        } else {
          monitoringMessage2 =
              'Sensor 2: Error al cargar los datos desde la API';
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
        ? 'http://192.168.1.71:8000/api/datos3/'
        : 'http://192.168.1.71:8000/api/datos3/'));

    print('Respuesta de la API: ${response.body}');

    if (response.statusCode == 200) {
      final List<Map<String, dynamic>> reportes =
          json.decode(response.body)['reportes'];

      // Filtrar reportes por collar_id == "1" o "2"
      final List<Map<String, dynamic>> filteredReportes = reportes
          .where((reporte) =>
              reporte['collar_id'] == "1" || reporte['collar_id'] == "2")
          .toList();

      if (filteredReportes.isNotEmpty) {
        return filteredReportes[0];
      } else {
        throw Exception('Datos no disponibles para collar_id 1 y 2');
      }
    } else {
      throw Exception('Error al cargar los datos desde la API');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            // Logo en la parte superior izquierda del visor de la API
            Image.asset('assets/logoNacional.png', height: 30, width: 30),
            SizedBox(width: 8),
            Text('Datos desde API'),
          ],
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                color: const Color.fromARGB(255, 59, 59, 59),
                borderRadius: BorderRadius.circular(10.0),
              ),
              child: Text(
                monitoringMessage1,
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: textColor1,
                  fontSize: 40,
                ),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => startMonitoringSensor1(context),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.all(16.0),
              ),
              child: Text(
                isMonitoring1
                    ? 'Sensor 1 (Cargando...)'
                    : 'Sensor 1 (desactivado)',
                style: TextStyle(fontSize: 25.0),
                textAlign: TextAlign.center,
              ),
            ),
            SizedBox(height: 20),
            Container(
              padding: EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                color: const Color.fromARGB(255, 59, 59, 59),
                borderRadius: BorderRadius.circular(10.0),
              ),
              child: Text(
                monitoringMessage2,
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: textColor2,
                  fontSize: 40,
                ),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => startMonitoringSensor2(context),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.all(16.0),
              ),
              child: Text(
                isMonitoring2
                    ? 'Sensor 2 (Cargando...)'
                    : 'Sensor 2 (desactivado)',
                style: TextStyle(fontSize: 25.0),
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
