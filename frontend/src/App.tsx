import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './layouts/MainLayout';
import { UploadPage } from './pages/UploadPage';
import { HistoryPage } from './pages/HistoryPage';
import { ResultPage } from './pages/ResultPage';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<MainLayout />}>
                    <Route index element={<UploadPage />} />
                    <Route path="historico" element={<HistoryPage />} />
                    <Route path="resultado/:id" element={<ResultPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
