<template>
  <div class="min-h-screen bg-[#090d16] text-slate-100 flex flex-col">
    <!-- Top Navbar -->
    <header class="border-b border-slate-800/80 bg-[#0d1322]/80 backdrop-blur sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-amber-600 flex items-center justify-center shadow-lg shadow-orange-500/20">
            <Server class="w-5 h-5 text-white" />
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <span class="font-bold text-lg text-white tracking-tight">OCI ARM Hunter</span>
              <span class="text-xs px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-400 border border-orange-500/20 font-medium">Osaka</span>
            </div>
            <p class="text-xs text-slate-400 hidden sm:block">quanglab-vps • Always Free A1.Flex</p>
          </div>
        </div>

        <!-- Right Header Actions -->
        <div class="flex items-center space-x-3">
          <!-- Status Pill -->
          <div :class="[
            'px-3 py-1.5 rounded-full text-xs font-semibold flex items-center space-x-2 border',
            status.success 
              ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
              : status.running 
                ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' 
                : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
          ]">
            <span class="relative flex h-2 w-2">
              <span v-if="status.running" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span :class="['relative inline-flex rounded-full h-2 w-2', status.success ? 'bg-emerald-400' : (status.running ? 'bg-amber-400' : 'bg-rose-400')]"></span>
            </span>
            <span>{{ status.success ? 'BẮT ĐƯỢC VPS!' : (status.running ? 'ĐANG SĂN (RUNNING)' : 'ĐANG TẮT (STOPPED)') }}</span>
          </div>

          <!-- Settings Button -->
          <button 
            @click="showSettings = !showSettings"
            class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors border border-slate-700"
            title="Cài đặt API Key"
          >
            <Key class="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full space-y-6">
      <!-- Settings Panel -->
      <div v-if="showSettings" class="p-4 rounded-xl bg-slate-900 border border-slate-700 shadow-xl transition-all">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-sm font-semibold text-white flex items-center space-x-2">
            <Key class="w-4 h-4 text-orange-400" />
            <span>Cấu hình kết nối Backend</span>
          </h3>
          <button @click="showSettings = false" class="text-xs text-slate-400 hover:text-white">Đóng</button>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-medium text-slate-400 mb-1">Backend API URL</label>
            <input 
              v-model="apiUrl" 
              type="text" 
              class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-sm text-white focus:outline-none focus:border-orange-500"
              placeholder="https://api-arm.quanglab.site"
            />
            <p class="text-[11px] text-slate-500 mt-1">Để <code>/api</code> nếu dùng rewrite qua Vercel.</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-400 mb-1">Secret API Key</label>
            <input 
              v-model="apiKey" 
              type="password" 
              class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-sm text-white focus:outline-none focus:border-orange-500"
              placeholder="quanglab-secret-2026"
            />
            <p class="text-[11px] text-slate-500 mt-1">Mật khẩu xác thực với Backend VPS.</p>
          </div>
        </div>
        <div class="mt-3 flex justify-end">
          <button @click="saveSettings" class="px-3 py-1.5 bg-orange-500 hover:bg-orange-600 text-white rounded-lg text-xs font-semibold transition-colors">
            Lưu cài đặt
          </button>
        </div>
      </div>

      <!-- Celebration Banner if Instance Created! -->
      <div v-if="status.success" class="p-6 rounded-2xl bg-gradient-to-r from-emerald-950/80 via-emerald-900/40 to-slate-900 border border-emerald-500/40 shadow-2xl shadow-emerald-500/10">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div class="flex items-center space-x-4">
            <div class="p-3 bg-emerald-500/20 text-emerald-400 rounded-2xl border border-emerald-500/30">
              <CheckCircle2 class="w-8 h-8" />
            </div>
            <div>
              <h2 class="text-xl font-bold text-white tracking-tight">🎉 BẮT ĐƯỢC VPS THÀNH CÔNG!</h2>
              <p class="text-sm text-emerald-200/80 mt-1">
                Instance <strong>{{ status.specs?.name || 'quanglab-vps' }}</strong> (2 OCPU / 12 GB RAM) đã được tạo trên Oracle Cloud Osaka!
              </p>
              <div v-if="status.instance_id" class="mt-2 text-xs font-mono text-emerald-300 break-all bg-black/40 px-3 py-1.5 rounded-lg border border-emerald-500/20">
                OCID: {{ status.instance_id }}
              </div>
            </div>
          </div>
          <a 
            :href="`https://cloud.oracle.com/compute/instances/${status.instance_id || ''}?region=ap-osaka-1`" 
            target="_blank" 
            class="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold rounded-xl text-sm transition-all shadow-lg shadow-emerald-500/25 flex items-center space-x-2 shrink-0"
          >
            <span>Mở Oracle Console</span>
            <ExternalLink class="w-4 h-4" />
          </a>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Attempts -->
        <div class="p-5 rounded-2xl bg-[#0e1424] border border-slate-800 shadow-sm relative overflow-hidden">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">Số lượt thử</span>
            <Repeat class="w-4 h-4 text-orange-400" />
          </div>
          <div class="flex items-baseline space-x-2">
            <span class="text-3xl font-extrabold text-white tracking-tight">{{ status.attempts }}</span>
            <span class="text-xs text-slate-500">lần thử</span>
          </div>
          <p class="text-xs text-slate-400 mt-2 truncate">Nhịp thử: 150 giây (2m30s)/lần</p>
        </div>

        <!-- Latest Status -->
        <div class="p-5 rounded-2xl bg-[#0e1424] border border-slate-800 shadow-sm relative overflow-hidden">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">Phản hồi gần nhất</span>
            <Activity class="w-4 h-4 text-blue-400" />
          </div>
          <div class="text-base font-bold text-white truncate" :title="status.last_status">
            {{ status.last_status || 'Chờ nhịp kế tiếp...' }}
          </div>
          <p class="text-xs text-slate-500 mt-2 truncate">Tự động bắt ngay khi có slot</p>
        </div>

        <!-- Specs Target -->
        <div class="p-5 rounded-2xl bg-[#0e1424] border border-slate-800 shadow-sm relative overflow-hidden">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">Cấu hình mục tiêu</span>
            <Cpu class="w-4 h-4 text-purple-400" />
          </div>
          <div class="text-base font-bold text-white">2 OCPU • 12 GB RAM</div>
          <p class="text-xs text-slate-400 mt-2">100 GB Boot Disk (Always Free)</p>
        </div>

        <!-- Target Region / Shape -->
        <div class="p-5 rounded-2xl bg-[#0e1424] border border-slate-800 shadow-sm relative overflow-hidden">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">Vùng & Kiến trúc</span>
            <Globe class="w-4 h-4 text-emerald-400" />
          </div>
          <div class="text-base font-bold text-white">ap-osaka-1 (AD-1)</div>
          <p class="text-xs text-slate-400 mt-2">VM.Standard.A1.Flex (ARM64)</p>
        </div>
      </div>

      <!-- Control Toolbar -->
      <div class="p-4 rounded-2xl bg-[#0e1424] border border-slate-800 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center space-x-3">
          <!-- Start Button -->
          <button 
            @click="startCatcher"
            :disabled="status.running || loading"
            :class="[
              'px-5 py-2.5 rounded-xl font-semibold text-sm flex items-center space-x-2 transition-all shadow-md',
              status.running 
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50' 
                : 'bg-gradient-to-r from-orange-500 to-amber-600 hover:from-orange-600 hover:to-amber-700 text-white shadow-orange-500/20 active:scale-95'
            ]"
          >
            <Play class="w-4 h-4 fill-current" />
            <span>Bật Săn (Start)</span>
          </button>

          <!-- Stop Button -->
          <button 
            @click="stopCatcher"
            :disabled="!status.running || loading"
            :class="[
              'px-5 py-2.5 rounded-xl font-semibold text-sm flex items-center space-x-2 transition-all border',
              !status.running 
                ? 'bg-slate-800/40 text-slate-600 border-slate-800 cursor-not-allowed' 
                : 'bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border-rose-500/30 active:scale-95'
            ]"
          >
            <Square class="w-4 h-4 fill-current" />
            <span>Dừng Săn (Stop)</span>
          </button>
        </div>

        <div class="flex items-center space-x-4">
          <!-- Auto-refresh switch -->
          <label class="flex items-center space-x-2 text-xs text-slate-400 cursor-pointer select-none">
            <input type="checkbox" v-model="autoRefresh" class="rounded bg-slate-800 border-slate-700 text-orange-500 focus:ring-0">
            <span>Tự làm mới (5s)</span>
          </label>

          <!-- Manual Refresh -->
          <button 
            @click="fetchData"
            :disabled="loading"
            class="p-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 transition-colors border border-slate-700/60 active:scale-95"
            title="Làm mới ngay"
          >
            <RefreshCw :class="['w-4 h-4', loading ? 'animate-spin text-orange-400' : '']" />
          </button>
        </div>
      </div>

      <!-- Terminal / Logs Viewer -->
      <div class="rounded-2xl bg-[#0a0f1d] border border-slate-800 overflow-hidden shadow-2xl flex flex-col">
        <!-- Terminal Header -->
        <div class="px-4 py-3 bg-[#0d1424] border-b border-slate-800 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 rounded-full bg-rose-500/80"></div>
            <div class="w-3 h-3 rounded-full bg-amber-500/80"></div>
            <div class="w-3 h-3 rounded-full bg-emerald-500/80"></div>
            <span class="text-xs text-slate-400 font-mono-code ml-2 flex items-center space-x-1.5">
              <Terminal class="w-3.5 h-3.5 text-slate-400" />
              <span>catcher.log</span>
            </span>
          </div>

          <div class="flex items-center space-x-3">
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer select-none">
              <input type="checkbox" v-model="autoScroll" class="rounded bg-slate-800 border-slate-700 text-orange-500 focus:ring-0">
              <span>Cuộn tự động</span>
            </label>
            <button 
              @click="copyLogs" 
              class="text-xs px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
            >
              {{ copied ? 'Đã sao chép!' : 'Copy log' }}
            </button>
          </div>
        </div>

        <!-- Terminal Body -->
        <div 
          ref="terminalBody"
          class="p-4 font-mono-code text-xs text-slate-300 h-96 overflow-y-auto space-y-1 bg-[#070b14]"
        >
          <div v-if="logs.length === 0" class="text-slate-600 italic py-4 text-center">
            Chưa có log. Bấm "Bật Săn" để khởi động catcher.
          </div>
          <div 
            v-for="(line, idx) in logs" 
            :key="idx" 
            :class="[
              'leading-relaxed break-all',
              line.includes('SUCCESS') ? 'text-emerald-400 font-bold bg-emerald-950/30 px-1 rounded' :
              line.includes('Attempt #') ? 'text-amber-300' :
              line.includes('Out of host capacity') ? 'text-rose-400/90' :
              line.includes('Error') ? 'text-rose-400' : 'text-slate-400'
            ]"
          >
            {{ line }}
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800/80 py-4 text-center text-xs text-slate-500">
      <span>OCI ARM Catcher Dashboard • Thiết lập tự động cho QuangLab</span>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { 
  Server, Play, Square, RefreshCw, Key, Terminal, 
  CheckCircle2, ExternalLink, Repeat, Activity, Cpu, Globe 
} from 'lucide-vue-next'

const apiUrl = ref(localStorage.getItem('oci_api_url') || import.meta.env.VITE_API_URL || '')
const apiKey = ref(localStorage.getItem('oci_api_key') || import.meta.env.VITE_API_KEY || '')
const showSettings = ref(false)
const autoRefresh = ref(true)
const autoScroll = ref(true)
const loading = ref(false)
const copied = ref(false)
const terminalBody = ref(null)

const status = ref({
  running: false,
  attempts: 0,
  success: false,
  instance_id: null,
  last_status: '',
  last_line: '',
  specs: null
})

const logs = ref([])
let refreshTimer = null

const getHeaders = () => {
  const headers = { 'Content-Type': 'application/json' }
  if (apiKey.value) headers['x-api-key'] = apiKey.value
  return headers
}

const saveSettings = () => {
  localStorage.setItem('oci_api_url', apiUrl.value)
  localStorage.setItem('oci_api_key', apiKey.value)
  showSettings.value = false
  fetchData()
}

const fetchData = async () => {
  if (!apiUrl.value) {
    showSettings.value = true
    return
  }
  loading.value = true
  try {
    const base = apiUrl.value.replace(/\/+$/, '')
    // 1. Fetch Status
    const statusRes = await fetch(`${base}/status`, { headers: getHeaders() })
    if (statusRes.ok) {
      status.value = await statusRes.json()
    } else if (statusRes.status === 401) {
      showSettings.value = true
    }

    // 2. Fetch Logs
    const logsRes = await fetch(`${base}/logs?lines=150`, { headers: getHeaders() })
    if (logsRes.ok) {
      const data = await logsRes.json()
      logs.value = data.logs || []
      if (autoScroll.value) {
        await nextTick()
        if (terminalBody.value) {
          terminalBody.value.scrollTop = terminalBody.value.scrollHeight
        }
      }
    }
  } catch (err) {
    console.error('Fetch error:', err)
  } finally {
    loading.value = false
  }
}

const startCatcher = async () => {
  loading.value = true
  try {
    const base = apiUrl.value.replace(/\/+$/, '')
    const res = await fetch(`${base}/start`, {
      method: 'POST',
      headers: getHeaders()
    })
    const data = await res.json()
    if (!res.ok) alert(data.detail || 'Không thể khởi động')
    await fetchData()
  } catch (err) {
    alert('Lỗi kết nối Backend: ' + err.message)
  } finally {
    loading.value = false
  }
}

const stopCatcher = async () => {
  if (!confirm('Bạn có chắc muốn dừng săn VPS?')) return
  loading.value = true
  try {
    const base = apiUrl.value.replace(/\/+$/, '')
    const res = await fetch(`${base}/stop`, {
      method: 'POST',
      headers: getHeaders()
    })
    const data = await res.json()
    if (!res.ok) alert(data.detail || 'Không thể dừng')
    await fetchData()
  } catch (err) {
    alert('Lỗi kết nối Backend: ' + err.message)
  } finally {
    loading.value = false
  }
}

const copyLogs = () => {
  navigator.clipboard.writeText(logs.value.join('\n'))
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

onMounted(() => {
  fetchData()
  refreshTimer = setInterval(() => {
    if (autoRefresh.value) {
      fetchData()
    }
  }, 5000)
})

onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
})
</script>
