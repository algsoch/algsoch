import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { AuthProvider } from './contexts/AuthContext';
import { WebSocketProvider } from './contexts/WebSocketContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Projects from './pages/Projects';
import Skills from './pages/Skills';
import Timeline from './pages/Timeline';
import Contact from './pages/Contact';
import Admin from './pages/Admin';
import AdminProjects from './pages/admin/AdminProjects';
import AdminSkills from './pages/admin/AdminSkills';
import AdminTimeline from './pages/admin/AdminTimeline';
import AdminBlogs from './pages/admin/AdminBlogs';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <WebSocketProvider>
          <BrowserRouter>
            <div className="min-h-screen flex flex-col">
              <Navbar />
              <main className="flex-grow">
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/projects" element={<Projects />} />
                  <Route path="/skills" element={<Skills />} />
                  <Route path="/timeline" element={<Timeline />} />
                  <Route path="/contact" element={<Contact />} />
                  <Route path="/admin" element={<Admin />} />
                  <Route path="/admin/projects" element={<AdminProjects />} />
                  <Route path="/admin/skills" element={<AdminSkills />} />
                  <Route path="/admin/timeline" element={<AdminTimeline />} />
                  <Route path="/admin/blogs" element={<AdminBlogs />} />
                </Routes>
              </main>
              <Footer />
            </div>
          </BrowserRouter>
        </WebSocketProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
