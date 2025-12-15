local M = {}

-- Handle Lua 5.1/5.2 compatibility (unpack moved to table.unpack in 5.3+)
local unpack = table.unpack or unpack

--- Opens file dialog, then creates love FileData objects and applies passed function on each.
---@param f function Function for FileData
---@param params table? Params for passed function
---@return nil
function M.processFiles(f, params)
  love.window.showFileDialog("openfile", function(filePaths, filtername, errorstring)
    if errorstring then
      print(errorstring)
      return
    end

    if filePaths then
      for _, filePath in ipairs(filePaths) do
        ---@type love.File
        local file = love.filesystem.openNativeFile(filePath, "r")
        if file then
          local fileData = file:read("data", file:getSize())
          file:close()

          f(fileData, unpack(params or {}))
        else
          print("Error: Could not open native file at " .. filePath)
        end
      end
    end
  end, {
    multiselect = true,
    acceptlabel = "Annotate",
    filters = { PNG = "png" },
  })
end

return M
