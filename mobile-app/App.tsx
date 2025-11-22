import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import HomeScreen from './src/screens/HomeScreen';
import ProjectsScreen from './src/screens/ProjectsScreen';
import SkillsScreen from './src/screens/SkillsScreen';
import TimelineScreen from './src/screens/TimelineScreen';
import ContactScreen from './src/screens/ContactScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator 
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#2563eb',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ title: 'ALGSOCH' }}
        />
        <Stack.Screen 
          name="Projects" 
          component={ProjectsScreen}
          options={{ title: 'Projects' }}
        />
        <Stack.Screen 
          name="Skills" 
          component={SkillsScreen}
          options={{ title: 'Skills' }}
        />
        <Stack.Screen 
          name="Timeline" 
          component={TimelineScreen}
          options={{ title: 'Timeline' }}
        />
        <Stack.Screen 
          name="Contact" 
          component={ContactScreen}
          options={{ title: 'Contact' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
