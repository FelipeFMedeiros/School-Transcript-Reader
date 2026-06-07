import { UploadZone } from '../components/UploadZone';

export const UploadPage = () => {
    return (
        <div className="flex-1 flex flex-col items-center justify-center animate-in fade-in duration-500">
            <div className="text-center mb-10 max-w-xl">
                <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl mb-4 text-gray-900">
                    Analisador de Histórico
                </h1>
                <p className="text-xl text-gray-500">
                    Faça o upload do seu histórico escolar do SIGAA para iniciarmos a extração de dados através do nosso
                    compilador.
                </p>
            </div>
            <UploadZone />
        </div>
    );
};
