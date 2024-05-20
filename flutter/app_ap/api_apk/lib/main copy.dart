import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:permission_handler/permission_handler.dart';

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
      Uri.parse('http://190.96.97.141:8001/api/login/'),
      body: {
        'username': usernameController.text,
        'password': passwordController.text,
      },
    );

    if (response.statusCode == 200) {
      // Autenticación exitosa, navegar a la pantalla principal
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => HomeScreen()),
      );
    } else {
      // Autenticación fallida, muestra un mensaje de error
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
            TextField(
              controller: usernameController,
              decoration: InputDecoration(labelText: 'Username'),
            ),
            TextField(
              controller: passwordController,
              obscureText: true,
              decoration: InputDecoration(labelText: 'Password'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => loginUser(context),
              child: Text('Iniciar sesión'),
            ),
          ],
        ),
      ),
    );
  }
}

class HomeScreen extends StatelessWidget {
  void startMonitoring(BuildContext context) {
    // Aquí puedes agregar la lógica para el monitoreo antes de ir a HomeScreen
    // ...

    // Muestra un mensaje temporal para simular la acción de monitoreo
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Iniciar monitoreo'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Datos desde API'),
        actions: [
          IconButton(
            icon: Icon(Icons.play_arrow),
            onPressed: () => startMonitoring(context),
            tooltip: 'Monitorear',
          ),
        ],
      ),
      body: Center(
        child: FutureBuilder(
          future: fetchData(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return CircularProgressIndicator();
            } else if (snapshot.hasError || snapshot.data == null) {
              return Text('Error: ${snapshot.error}');
            } else {
              // Mostrar los datos en el centro
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('Temperatura: ${snapshot.data?['temperatura']}°C'),
                    Text('Humedad: ${snapshot.data?['humedad']}%'),
                    Text('Pulsaciones: ${snapshot.data?['pulsaciones']}'),
                  ],
                ),
              );
            }
          },
        ),
      ),
    );
  }

  Future<Map<String, dynamic>?> fetchData() async {
    final response =
        await http.get(Uri.parse('http://190.96.97.141:8001/api/datos3/'));
    if (response.statusCode == 200) {
      return json.decode(response.body)['reportes'][0];
    } else {
      throw Exception('Error al cargar los datos desde la API');
    }
  }
}
