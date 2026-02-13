import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:ufanga/theme.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  FlutterError.onError = (details) {
    // Print Flutter framework errors to console for diagnosis
    debugPrint('FlutterError: ${details.exceptionAsString()}');
    debugPrint(details.stack.toString());
  };
  debugPrint('main: starting runApp');
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  String _fontKey = 'openSans';
  bool _fontsReady = false;

  void _setFont(String? key) {
    if (key == null) return;
    setState(() {
      _fontKey = key;
    });
    _saveFontPref(key);
  }
    

  @override
  void initState() {
    super.initState();
    _loadFontPref();
    // Delay using GoogleFonts-based ThemeData until after first frame so
    // AssetManifest.json is available and GoogleFonts won't try to read it too early.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      setState(() {
        _fontsReady = true;
      });
    });
  }

  Future<void> _loadFontPref() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final saved = prefs.getString('selectedFontKey');
      if (saved != null && saved.isNotEmpty) {
        setState(() {
          _fontKey = saved;
        });
      }
    } catch (_) {}
  }

  Future<void> _saveFontPref(String key) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('selectedFontKey', key);
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    // Use a lightweight fallback theme until fonts are ready.
    final ThemeData lightFallback = ThemeData(
      brightness: Brightness.light,
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.lightGray,
      colorScheme: ColorScheme.light(
        primary: AppColors.primary,
        secondary: AppColors.secondary,
        background: AppColors.lightGray,
        surface: AppColors.card,
      ),
    );

    final ThemeData darkFallback = ThemeData(
      brightness: Brightness.dark,
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.background,
      colorScheme: ColorScheme.dark(
        primary: AppColors.primary,
        secondary: AppColors.secondary,
        background: AppColors.background,
        surface: AppColors.card,
      ),
    );

    return MaterialApp(
      title: 'Flutter Demo',
      theme: _fontsReady ? ThemeManager.themeForFont(_fontKey, Brightness.light) : lightFallback,
      darkTheme: _fontsReady ? ThemeManager.themeForFont(_fontKey, Brightness.dark) : darkFallback,
      themeMode: ThemeMode.system,
      home: MyHomePage(
        title: 'Flutter Demo Home Page',
        fontKey: _fontKey,
        onFontChanged: _setFont,
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title, required this.fontKey, required this.onFontChanged});

  final String title;
  final String fontKey;
  final ValueChanged<String?> onFontChanged;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle(
      statusBarColor: colorScheme.background,
      statusBarIconBrightness: Theme.of(context).brightness == Brightness.dark ? Brightness.light : Brightness.dark,
      systemNavigationBarColor: colorScheme.background,
      systemNavigationBarIconBrightness: Theme.of(context).brightness == Brightness.dark ? Brightness.light : Brightness.dark,
    ));

    return Scaffold(
      // remove default AppBar; make background extend to system bars
      extendBody: true,
      body: MediaQuery.removePadding(
        context: context,
        removeTop: true,
        child: Container(
          color: colorScheme.background,
          width: double.infinity,
          height: double.infinity,
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Font selector
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('Font: '),
                      const SizedBox(width: 8),
                      DropdownButton<String>(
                        value: widget.fontKey,
                        items: const [
                          DropdownMenuItem(value: 'luckiestGuy', child: Text('Luckiest Guy')),
                          DropdownMenuItem(value: 'ubuntu', child: Text('Ubuntu')),
                          DropdownMenuItem(value: 'anton', child: Text('Anton')),
                          DropdownMenuItem(value: 'allan', child: Text('Allan')),
                          DropdownMenuItem(value: 'bangers', child: Text('Bangers')),
                          DropdownMenuItem(value: 'cookie', child: Text('Cookie')),
                          DropdownMenuItem(value: 'openSans', child: Text('Open Sans')),
                          DropdownMenuItem(value: 'josefinSans', child: Text('Josefin Sans')),
                        ],
                        onChanged: widget.onFontChanged,
                      ),
                    ],
                  ),
                ),
                const Text('You have pushed the button this many times:'),
                Text(
                  '$_counter',
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
              ],
            ),
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
