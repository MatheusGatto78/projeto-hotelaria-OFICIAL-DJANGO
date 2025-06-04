document.addEventListener('DOMContentLoaded', () => {
    const dragDropZone = document.getElementById('drag-drop-zone');
    // Encontra o input de arquivo real renderizado pelo form.img do Django dentro da área de drag-drop
    const fileInput = dragDropZone.querySelector('input[type="file"]');

    // Previne comportamentos padrão do navegador para eventos de arrastar (como abrir o arquivo arrastado)
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dragDropZone.addEventListener(eventName, preventDefaults, false);
        // Também previne o comportamento padrão para o corpo do documento para lidar
        // com arrastar arquivos fora da zona de soltar, mas ainda na página
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Adiciona/remove a classe 'dragover' para feedback visual
    ['dragenter', 'dragover'].forEach(eventName => {
        dragDropZone.addEventListener(eventName, () => {
            dragDropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dragDropZone.addEventListener(eventName, () => {
            dragDropZone.classList.remove('dragover');
        }, false);
    });

    // Lida com arquivos soltos
    dragDropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files; // Obtém o objeto FileList

        if (files.length > 0) {
            // Atribui os arquivos soltos à propriedade 'files' do input oculto
            fileInput.files = files; 
            
            // Dispara um evento 'change' manualmente, pois atribuir arquivos diretamente
            // nem sempre o aciona automaticamente. Isso é uma boa prática
            // se o seu framework ou outros scripts dependem do evento 'change'.
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);

            // Exibe uma pré-visualização da primeira imagem solta
            displayImagePreview(files[0]);
        }
    }

    // Permite clicar na zona personalizada para abrir a caixa de diálogo de seleção de arquivo
    dragDropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Lida com a seleção de arquivo quando o usuário clica no input oculto e seleciona arquivos
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            displayImagePreview(fileInput.files[0]);
        }
    });

    // Função para exibir a pré-visualização da imagem
    function displayImagePreview(file) {
        // Garante que o arquivo seja uma imagem antes de tentar exibi-lo
        if (!file.type.startsWith('image/')) {
            console.warn("O arquivo não é uma imagem. Não é possível exibir a pré-visualização.");
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            // Remove qualquer pré-visualização existente para mostrar apenas a imagem selecionada mais recente
            const existingPreview = dragDropZone.querySelector('.image-preview');
            if (existingPreview) {
                existingPreview.remove();
            }

            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('image-preview');
            
            // Oculta o texto inicial de "arrastar e soltar"
            const paragraph = dragDropZone.querySelector('p');
            if (paragraph) {
                paragraph.style.display = 'none';
            }
            
            dragDropZone.appendChild(img);
        };
        reader.readAsDataURL(file); // Lê o arquivo como uma URL de dados para pré-visualização
    }
});