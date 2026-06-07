import { Outlet, Link, useLocation } from 'react-router-dom';
import { Upload, Clock, GraduationCap } from 'lucide-react';

export const MainLayout = () => {
    const location = useLocation();

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            <nav className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex items-center gap-2">
                            <GraduationCap className="h-8 w-8 text-primary" />
                            <span className="font-bold text-xl text-gray-900">Transcript Reader</span>
                        </div>
                        {/* Barra de Navegação principal */}
                        <div className="flex items-center space-x-6">
                            <Link
                                to="/"
                                className={`flex items-center gap-2 px-3 py-2 rounded-md font-medium transition-colors 
                                  ${
                                      location.pathname === '/'
                                          ? 'text-primary bg-primary/10 cursor-default underline underline-offset-4'
                                          : 'text-gray-600 hover:text-primary hover:bg-gray-50'
                                  }`}
                            >
                                <Upload className="h-4 w-4" />
                                Novo Upload
                            </Link>
                            <Link
                                to="/historico"
                                className={`flex items-center gap-2 px-3 py-2 rounded-md font-medium transition-colors 
                                  ${
                                      location.pathname === '/historico'
                                          ? 'text-primary bg-primary/10 cursor-default underline underline-offset-4'
                                          : 'text-gray-600 hover:text-primary hover:bg-gray-50'
                                  }`}
                            >
                                <Clock className="h-4 w-4" />
                                Histórico
                            </Link>
                        </div>
                    </div>
                </div>
            </nav>
            <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 flex flex-col">
                <Outlet />
            </main>
        </div>
    );
};
