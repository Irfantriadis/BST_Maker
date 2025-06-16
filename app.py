import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass
from typing import Optional, List, Tuple
import math
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="BST Maker - Binary Search Tree Visualizer",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling yang lebih menarik
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .bg-toggle-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        margin: 0.5rem 0;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class TreeNode:
    """Node untuk Binary Search Tree"""
    value: int
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None
    x: float = 0.0
    y: float = 0.0
    color: str = "#4CAF50"

class BST:
    """Binary Search Tree class dengan visualisasi"""
    
    def __init__(self, allow_duplicates: bool = False):
        self.root: Optional[TreeNode] = None
        self.animation_steps = []
        self.allow_duplicates = allow_duplicates
        
    def insert(self, value: int) -> List[str]:
        """Insert value ke BST dan return langkah-langkah"""
        steps = []
        if self.root is None:
            self.root = TreeNode(value)
            steps.append(f"🌱 Membuat root node dengan nilai {value}")
        else:
            self._insert_recursive(self.root, value, steps, "root")
        
        self._calculate_positions()
        return steps
    
    def _insert_recursive(self, node: TreeNode, value: int, steps: List[str], position: str):
        """Helper untuk insert recursive"""
        if value < node.value:
            steps.append(f"📍 {value} < {node.value}, pergi ke kiri dari {position}")
            if node.left is None:
                node.left = TreeNode(value)
                steps.append(f"✅ Menyisipkan {value} sebagai anak kiri dari {node.value}")
            else:
                self._insert_recursive(node.left, value, steps, f"kiri-{node.value}")
        elif value > node.value:
            steps.append(f"📍 {value} > {node.value}, pergi ke kanan dari {position}")
            if node.right is None:
                node.right = TreeNode(value)
                steps.append(f"✅ Menyisipkan {value} sebagai anak kanan dari {node.value}")
            else:
                self._insert_recursive(node.right, value, steps, f"kanan-{node.value}")
        else:
            if self.allow_duplicates:
                steps.append(f"🔄 Nilai {value} sudah ada, tapi duplikat diizinkan - menambah ke kanan")
                if node.right is None:
                    node.right = TreeNode(value)
                    steps.append(f"✅ Menyisipkan duplikat {value} sebagai anak kanan dari {node.value}")
                else:
                    self._insert_recursive(node.right, value, steps, f"kanan-{node.value}")
            else:
                steps.append(f"⚠️ Nilai {value} sudah ada dalam tree! (Duplikat tidak diizinkan)")
    
    def search(self, value: int) -> Tuple[bool, List[str]]:
        """Cari value dalam BST dan return hasil + langkah"""
        steps = []
        found = self._search_recursive(self.root, value, steps, "root")
        return found, steps
    
    def _search_recursive(self, node: Optional[TreeNode], value: int, steps: List[str], position: str) -> bool:
        """Helper untuk search recursive"""
        if node is None:
            steps.append(f"❌ Nilai {value} tidak ditemukan!")
            return False
        
        steps.append(f"🔍 Mengecek node {position} dengan nilai {node.value}")
        
        if value == node.value:
            steps.append(f"🎉 Nilai {value} ditemukan di {position}!")
            return True
        elif value < node.value:
            steps.append(f"📍 {value} < {node.value}, mencari di subtree kiri")
            return self._search_recursive(node.left, value, steps, f"kiri-{node.value}")
        else:
            steps.append(f"📍 {value} > {node.value}, mencari di subtree kanan")
            return self._search_recursive(node.right, value, steps, f"kanan-{node.value}")
    
    def delete(self, value: int) -> List[str]:
        """Hapus value dari BST"""
        steps = []
        self.root = self._delete_recursive(self.root, value, steps)
        self._calculate_positions()
        return steps
    
    def _delete_recursive(self, node: Optional[TreeNode], value: int, steps: List[str]) -> Optional[TreeNode]:
        """Helper untuk delete recursive"""
        if node is None:
            steps.append(f"❌ Nilai {value} tidak ditemukan untuk dihapus!")
            return None
        
        if value < node.value:
            steps.append(f"📍 Mencari {value} di subtree kiri dari {node.value}")
            node.left = self._delete_recursive(node.left, value, steps)
        elif value > node.value:
            steps.append(f"📍 Mencari {value} di subtree kanan dari {node.value}")
            node.right = self._delete_recursive(node.right, value, steps)
        else:
            steps.append(f"🎯 Menemukan node {value} untuk dihapus")
            
            # Node dengan 0 atau 1 anak
            if node.left is None:
                steps.append(f"➡️ Node {value} tidak memiliki anak kiri, mengganti dengan anak kanan")
                return node.right
            elif node.right is None:
                steps.append(f"⬅️ Node {value} tidak memiliki anak kanan, mengganti dengan anak kiri")
                return node.left
            
            # Node dengan 2 anak
            steps.append(f"🔄 Node {value} memiliki 2 anak, mencari successor")
            successor = self._find_min(node.right)
            steps.append(f"✅ Successor ditemukan: {successor.value}")
            
            node.value = successor.value
            steps.append(f"🔄 Mengganti nilai {value} dengan {successor.value}")
            
            node.right = self._delete_recursive(node.right, successor.value, steps)
        
        return node
    
    def _find_min(self, node: TreeNode) -> TreeNode:
        """Cari node dengan nilai minimum"""
        while node.left is not None:
            node = node.left
        return node
    
    def get_traversals(self) -> dict:
        """Dapatkan hasil traversal dalam berbagai cara"""
        traversals = {
            'inorder': [],
            'preorder': [],
            'postorder': []
        }
        
        self._inorder(self.root, traversals['inorder'])
        self._preorder(self.root, traversals['preorder'])
        self._postorder(self.root, traversals['postorder'])
        
        return traversals
    
    def _inorder(self, node: Optional[TreeNode], result: List[int]):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)
    
    def _preorder(self, node: Optional[TreeNode], result: List[int]):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)
    
    def _postorder(self, node: Optional[TreeNode], result: List[int]):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)
    
    def get_height(self) -> int:
        """Dapatkan tinggi tree"""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))
    
    def get_node_count(self) -> int:
        """Dapatkan jumlah node"""
        return self._count_nodes(self.root)
    
    def _count_nodes(self, node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)
    
    def _calculate_positions(self):
        """Hitung posisi node untuk visualisasi"""
        if self.root is None:
            return
        
        # Hitung lebar total yang dibutuhkan
        height = self.get_height()
        width = 2 ** height
        
        self._assign_positions(self.root, 0, width, height - 1)
    
    def _assign_positions(self, node: TreeNode, left: float, right: float, level: int):
        """Assign posisi x,y untuk setiap node"""
        if node is None:
            return
        
        node.x = (left + right) / 2
        node.y = level
        
        mid = (left + right) / 2
        if node.left:
            self._assign_positions(node.left, left, mid, level - 1)
        if node.right:
            self._assign_positions(node.right, mid, right, level - 1)

def create_tree_visualization(bst: BST, dark_mode: bool = True) -> go.Figure:
    """Buat visualisasi tree menggunakan Plotly dengan opsi background"""
    
    # Tentukan warna berdasarkan mode
    if dark_mode:
        bg_color = '#1e1e1e'
        paper_bg = '#2d2d2d'
        text_color = 'white'
        edge_color = '#E0E0E0'
        empty_text_color = '#cccccc'
        title_color = '#ffffff'
    else:
        bg_color = 'white'
        paper_bg = '#f8f9fa'
        text_color = 'black'
        edge_color = '#666666'
        empty_text_color = '#666666'
        title_color = '#2E4057'
    
    if bst.root is None:
        fig = go.Figure()
        fig.add_annotation(
            text="🌳 Tree kosong - Tambahkan node pertama!",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20, color=empty_text_color)
        )
        fig.update_layout(
            title=dict(
                text="🌳 Binary Search Tree Visualization",
                font=dict(size=20, color=title_color)
            ),
            showlegend=False,
            height=500,
            paper_bgcolor=paper_bg,
            plot_bgcolor=bg_color,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        return fig
    
    # Kumpulkan semua node
    nodes = []
    edges = []
    
    def collect_nodes(node: TreeNode):
        if node is None:
            return
        
        nodes.append({
            'x': node.x,
            'y': node.y,
            'value': node.value,
            'color': node.color
        })
        
        if node.left:
            edges.append({
                'x0': node.x, 'y0': node.y,
                'x1': node.left.x, 'y1': node.left.y
            })
            collect_nodes(node.left)
        
        if node.right:
            edges.append({
                'x0': node.x, 'y0': node.y,
                'x1': node.right.x, 'y1': node.right.y
            })
            collect_nodes(node.right)
    
    collect_nodes(bst.root)
    
    fig = go.Figure()
    
    # Tambahkan edges (garis penghubung)
    for edge in edges:
        fig.add_trace(go.Scatter(
            x=[edge['x0'], edge['x1']],
            y=[edge['y0'], edge['y1']],
            mode='lines',
            line=dict(color=edge_color, width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Tambahkan nodes
    x_vals = [node['x'] for node in nodes]
    y_vals = [node['y'] for node in nodes]
    values = [node['value'] for node in nodes]
    colors = [node['color'] for node in nodes]
    
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='markers+text',
        marker=dict(
            size=40,
            color=colors,
            line=dict(width=3, color='white'),
            opacity=0.9
        ),
        text=values,
        textfont=dict(size=14, color='white'),
        textposition='middle center',
        showlegend=False,
        hovertemplate='<b>Node: %{text}</b><br>Level: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="🌳 Binary Search Tree Visualization",
            font=dict(size=20, color=title_color)
        ),
        showlegend=False,
        height=500,
        paper_bgcolor=paper_bg,
        plot_bgcolor=bg_color,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def main():
    # Header utama
    st.markdown("""
    <div class="main-header">
        <h1>🌳 BST Maker - Binary Search Tree Visualizer</h1>
        <p>Aplikasi interaktif untuk belajar dan memvisualisasikan Binary Search Tree</p>
        <p>by irfantriadis_</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'bst' not in st.session_state:
        st.session_state.bst = BST()
    if 'operation_history' not in st.session_state:
        st.session_state.operation_history = []
    if 'allow_duplicates' not in st.session_state:
        st.session_state.allow_duplicates = False
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True
    
    # Sidebar untuk kontrol
    with st.sidebar:
        st.header("🎮 Kontrol BST")
        
        # Pengaturan BST
        st.subheader("⚙️ Pengaturan")
        
        # Toggle untuk background canvas
        st.markdown("#### 🎨 Background Canvas")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌙 Dark", key="dark_mode_btn", help="Background gelap"):
                st.session_state.dark_mode = True
                st.rerun()
        
        with col2:
            if st.button("☀️ Light", key="light_mode_btn", help="Background terang"):
                st.session_state.dark_mode = False
                st.rerun()
        
        # Status mode saat ini
        mode_text = "🌙 Dark Mode" if st.session_state.dark_mode else "☀️ Light Mode"
        st.info(f"Mode saat ini: {mode_text}")
        
        # Checkbox untuk duplikat
        new_allow_duplicates = st.checkbox("🔄 Izinkan Duplikat", value=st.session_state.allow_duplicates, 
                                          help="Jika dicentang, nilai yang sama bisa ditambahkan ke tree")
        
        if new_allow_duplicates != st.session_state.allow_duplicates:
            st.session_state.allow_duplicates = new_allow_duplicates
            st.session_state.bst.allow_duplicates = new_allow_duplicates
            st.session_state.operation_history.append(f"⚙️ Pengaturan duplikat: {'Diizinkan' if new_allow_duplicates else 'Tidak diizinkan'}")
        
        st.markdown("---")
        
        # Insert node
        st.subheader("➕ Tambah Node")
        insert_value = st.number_input("Nilai untuk ditambahkan:", min_value=-1000, max_value=1000, value=0, key="insert_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌱 Insert", key="insert_btn"):
                steps = st.session_state.bst.insert(insert_value)
                st.session_state.operation_history.extend(steps)
                st.rerun()
        
        with col2:
            if st.button("🎲 Random", key="random_btn"):
                import random
                random_val = random.randint(1, 100)
                steps = st.session_state.bst.insert(random_val)
                st.session_state.operation_history.extend(steps)
                st.rerun()
        
        # Search node
        st.subheader("🔍 Cari Node")
        search_value = st.number_input("Nilai untuk dicari:", min_value=-1000, max_value=1000, value=0, key="search_input")
        
        if st.button("🔎 Search", key="search_btn"):
            found, steps = st.session_state.bst.search(search_value)
            st.session_state.operation_history.extend(steps)
            if found:
                st.success(f"✅ Nilai {search_value} ditemukan!")
            else:
                st.error(f"❌ Nilai {search_value} tidak ditemukan!")
        
        # Delete node
        st.subheader("🗑️ Hapus Node")
        delete_value = st.number_input("Nilai untuk dihapus:", min_value=-1000, max_value=1000, value=0, key="delete_input")
        
        if st.button("🚮 Delete", key="delete_btn"):
            steps = st.session_state.bst.delete(delete_value)
            st.session_state.operation_history.extend(steps)
            st.rerun()
        
        # Quick actions
        st.subheader("⚡ Aksi Cepat")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔥 Clear All", key="clear_btn"):
                st.session_state.bst = BST(allow_duplicates=st.session_state.allow_duplicates)
                st.session_state.operation_history = ["🧹 Tree telah dikosongkan!"]
                st.rerun()
        
        with col2:
            if st.button("📝 Sample Data", key="sample_btn"):
                sample_values = [50, 30, 70, 20, 40, 60, 80]
                for val in sample_values:
                    st.session_state.bst.insert(val)
                st.session_state.operation_history.append("📊 Sample data telah dimuat: " + str(sample_values))
                st.rerun()
    
    # Layout utama
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Visualisasi tree
        st.subheader("🎨 Visualisasi Tree")
        fig = create_tree_visualization(st.session_state.bst, st.session_state.dark_mode)
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistik BST
        if st.session_state.bst.root is not None:
            traversals = st.session_state.bst.get_traversals()
            
            st.subheader("📊 Traversal Results")
            
            tab1, tab2, tab3 = st.tabs(["🔄 Inorder", "⬇️ Preorder", "⬆️ Postorder"])
            
            with tab1:
                st.markdown(f"""
                <div class="info-box">
                    <h4>Inorder Traversal (Left → Root → Right)</h4>
                    <p><strong>Hasil:</strong> {' → '.join(map(str, traversals['inorder']))}</p>
                    <p><em>Inorder menghasilkan nilai dalam urutan terurut! 
                    {'(Duplikat akan muncul beberapa kali)' if st.session_state.allow_duplicates else ''}</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            with tab2:
                st.markdown(f"""
                <div class="info-box">
                    <h4>Preorder Traversal (Root → Left → Right)</h4>
                    <p><strong>Hasil:</strong> {' → '.join(map(str, traversals['preorder']))}</p>
                    <p><em>Preorder berguna untuk menyalin tree!</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            with tab3:
                st.markdown(f"""
                <div class="info-box">
                    <h4>Postorder Traversal (Left → Right → Root)</h4>
                    <p><strong>Hasil:</strong> {' → '.join(map(str, traversals['postorder']))}</p>
                    <p><em>Postorder berguna untuk menghapus tree!</em></p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # Statistik BST
        st.subheader("📈 Statistik BST")
        
        height = st.session_state.bst.get_height()
        node_count = st.session_state.bst.get_node_count()
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏔️ Tinggi Tree</h3>
            <h2>{height}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔢 Jumlah Node</h3>
            <h2>{node_count}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # History operasi
        st.subheader("📜 History Operasi")
        
        if st.button("🧹 Clear History"):
            st.session_state.operation_history = []
            st.rerun()
        
        # Tampilkan history dalam container yang bisa di-scroll
        if st.session_state.operation_history:
            history_container = st.container()
            with history_container:
                # Tampilkan 10 operasi terakhir
                recent_history = st.session_state.operation_history[-10:]
                for i, step in enumerate(reversed(recent_history)):
                    st.text(f"{len(recent_history)-i}. {step}")
        else:
            st.info("Belum ada operasi yang dilakukan")
    
    # Footer dengan informasi tambahan
    st.markdown("---")
    
    with st.expander("📚 Tentang Binary Search Tree"):
        st.markdown("""
        **Binary Search Tree (BST)** adalah struktur data tree di mana:
        
        1. **Setiap node memiliki maksimal 2 anak** (kiri dan kanan)
        2. **Semua nilai di subtree kiri < nilai node**
        3. **Semua nilai di subtree kanan > nilai node**
        4. **Kedua subtree juga merupakan BST**
        
        **Keunggulan BST:**
        - ✅ Pencarian efisien: O(log n) average case
        - ✅ Insert dan delete: O(log n) average case  
        - ✅ Inorder traversal menghasilkan urutan terurut
        - ✅ Struktur data dinamis
        - ✅ Dapat dikonfigurasi untuk menerima duplikat
        
        **Kelemahan BST:**
        - ❌ Worst case O(n) jika tidak seimbang
        - ❌ Tidak ada jaminan keseimbangan otomatis
        
        **Handling Duplikat:**
        - 🔄 **Mode Duplikat Diizinkan**: Nilai sama ditambahkan ke subtree kanan
        - ⚠️ **Mode Duplikat Ditolak**: Nilai sama akan diabaikan (BST tradisional)
        
        **Tips Penggunaan:**
        - Gunakan untuk data yang sering dicari
        - Pertimbangkan Self-Balancing BST (AVL, Red-Black) untuk dataset besar
        - Ideal untuk range queries dan ordered statistics
        - Aktifkan duplikat jika data Anda memiliki nilai berulang
        
        **Fitur Background:**
        - 🌙 **Dark Mode**: Background gelap untuk kenyamanan mata
        - ☀️ **Light Mode**: Background terang untuk presentasi yang lebih cerah
        """)
    
    # Credit
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>Dibuat dengan menggunakan Streamlit & Plotly</p>
        <p><strong>App by irfantriadis_</strong></p>
        <p>BST Maker - Belajar struktur data dengan visualisasi interaktif!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
